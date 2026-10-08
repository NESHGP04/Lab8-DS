#!/usr/bin/env python3
"""Benchmark: Parquet directo vs tabla materializada en DuckDB.

Ejecuta un conjunto de consultas representativas sobre ambas estrategias,
variando el volumen de datos, y registra los tiempos de ejecucion.

Uso:
    python scripts/benchmark.py                 # corre todo
    python scripts/benchmark.py --repeats 3     # menos repeticiones (rapido)

Requisito: ejecutar antes  python scripts/build_duckdb.py
"""

import argparse
import csv
import statistics
import time
from pathlib import Path

import duckdb

# ── Configuracion ───────────────────────────────────────────────────
DB_PATH = "data/processed/taxis.duckdb"
RESULTS_CSV = Path("data/processed/benchmark_results.csv")
DEFAULT_REPEATS = 5

# Volumenes de datos a probar (globs de Parquet).
# Cada entrada: (etiqueta, glob_pattern)
VOLUMENES = [
    ("1 mes (yellow ene-2024)",   "data/raw/yellow/2024/yellow_tripdata_2024-01.parquet"),
    ("3 meses (yellow ene–mar 2024)", "data/raw/yellow/2024/yellow_tripdata_2024-0[1-3].parquet"),
    ("1 anio (yellow 2024)",      "data/raw/yellow/2024/*.parquet"),
    ("Todo (yellow+green 2024+2026)", "data/raw/*/*/*.parquet"),
]

# Consultas de benchmark.
# Cada entrada: (nombre, sql_parquet_template, sql_tabla)
# En sql_parquet_template:
#   {glob}       → glob de Parquet del volumen
#   {pickup_expr} → expresion para pickup datetime (varia segun si hay solo yellow o mixed)
QUERIES = [
    (
        "Q1 Agregacion",
        # ── Parquet ──
        """SELECT
               regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
               TRY_CAST(regexp_extract(filename, '(20[0-9]{{2}})-[0-9]{{2}}\\.parquet$', 1) AS INTEGER) AS anio,
               count(*) AS viajes,
               round(avg(TRY_CAST(total_amount AS DOUBLE)), 2) AS total_promedio
           FROM read_parquet('{glob}', union_by_name=true, filename=true, hive_partitioning=false)
           GROUP BY 1, 2 ORDER BY 2, 1""",
        # ── Tabla ──
        """SELECT tipo, anio_archivo AS anio, count(*) AS viajes,
                  round(avg(total), 2) AS total_promedio
           FROM viajes {where} GROUP BY 1, 2 ORDER BY 2, 1""",
    ),
    (
        "Q2 Filtro",
        """SELECT
               regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
               count(*) AS viajes_largos,
               round(avg(TRY_CAST(fare_amount AS DOUBLE)), 2) AS tarifa_promedio
           FROM read_parquet('{glob}', union_by_name=true, filename=true, hive_partitioning=false)
           WHERE TRY_CAST(trip_distance AS DOUBLE) > 10
           GROUP BY 1 ORDER BY 1""",
        """SELECT tipo, count(*) AS viajes_largos,
                  round(avg(tarifa), 2) AS tarifa_promedio
           FROM viajes WHERE distancia_millas > 10 {and_where}
           GROUP BY 1 ORDER BY 1""",
    ),
    (
        "Q3 Temporal",
        """SELECT
               date_trunc('month', {pickup_expr})::DATE AS mes,
               count(*) AS viajes
           FROM read_parquet('{glob}', union_by_name=true, filename=true, hive_partitioning=false)
           WHERE {pickup_expr} IS NOT NULL
           GROUP BY 1 ORDER BY 1""",
        """SELECT date_trunc('month', inicio)::DATE AS mes, count(*) AS viajes
           FROM viajes WHERE inicio IS NOT NULL {and_where}
           GROUP BY 1 ORDER BY 1""",
    ),
    (
        "Q4 JOIN zonas",
        """SELECT z.Zone AS zona, z.Borough AS borough, count(*) AS viajes
           FROM read_parquet('{glob}', union_by_name=true, filename=true, hive_partitioning=false) t
           JOIN read_csv_auto('data/raw/zonas/taxi_zone_lookup.csv') z
             ON TRY_CAST(t.PULocationID AS INTEGER) = z.LocationID
           GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 10""",
        """SELECT z.Zone AS zona, z.Borough AS borough, count(*) AS viajes
           FROM viajes v JOIN zonas z ON v.zona_recogida = z.LocationID
           {where} GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 10""",
    ),
    (
        "Q5 Top-N window",
        """WITH diario AS (
               SELECT TRY_CAST(regexp_extract(filename, '(20[0-9]{{2}})-[0-9]{{2}}\\.parquet$', 1) AS INTEGER) AS anio,
                      CAST({pickup_expr} AS DATE) AS dia,
                      count(*) AS viajes
               FROM read_parquet('{glob}', union_by_name=true, filename=true, hive_partitioning=false)
               WHERE {pickup_expr} IS NOT NULL
               GROUP BY 1, 2),
           ranked AS (SELECT *, row_number() OVER (PARTITION BY anio ORDER BY viajes DESC) AS rn FROM diario)
           SELECT anio, dia, viajes FROM ranked WHERE rn <= 5 ORDER BY anio, rn""",
        """WITH diario AS (
               SELECT anio_archivo AS anio, CAST(inicio AS DATE) AS dia, count(*) AS viajes
               FROM viajes WHERE inicio IS NOT NULL {and_where} GROUP BY 1, 2),
           ranked AS (SELECT *, row_number() OVER (PARTITION BY anio ORDER BY viajes DESC) AS rn FROM diario)
           SELECT anio, dia, viajes FROM ranked WHERE rn <= 5 ORDER BY anio, rn""",
    ),
]

# Expresiones de pickup datetime segun si los archivos son solo yellow o mixtos.
PICKUP_YELLOW_ONLY = "TRY_CAST(tpep_pickup_datetime AS TIMESTAMP)"
PICKUP_MIXED = ("COALESCE(TRY_CAST(tpep_pickup_datetime AS TIMESTAMP), "
                "TRY_CAST(lpep_pickup_datetime AS TIMESTAMP))")


def _where_for_volume(etiqueta: str) -> tuple[str, str, str]:
    """Genera clausulas WHERE/AND y la expresion de pickup para filtrar
    la tabla materializada de modo que sea equivalente al glob del volumen.
    Devuelve (where, and_where, pickup_expr)."""
    if "ene-2024" in etiqueta:
        w = "WHERE tipo = 'yellow' AND anio_archivo = 2024 AND month(inicio) = 1"
        a = "AND tipo = 'yellow' AND anio_archivo = 2024 AND month(inicio) = 1"
        p = PICKUP_YELLOW_ONLY
    elif "ene–mar 2024" in etiqueta or "ene-mar 2024" in etiqueta:
        w = "WHERE tipo = 'yellow' AND anio_archivo = 2024 AND month(inicio) BETWEEN 1 AND 3"
        a = "AND tipo = 'yellow' AND anio_archivo = 2024 AND month(inicio) BETWEEN 1 AND 3"
        p = PICKUP_YELLOW_ONLY
    elif "yellow 2024" in etiqueta:
        w = "WHERE tipo = 'yellow' AND anio_archivo = 2024"
        a = "AND tipo = 'yellow' AND anio_archivo = 2024"
        p = PICKUP_YELLOW_ONLY
    else:  # Todo (yellow + green)
        w = ""
        a = ""
        p = PICKUP_MIXED
    return w, a, p


def run_query(con: duckdb.DuckDBPyConnection, sql: str) -> None:
    """Ejecuta la consulta y consume todos los resultados."""
    con.execute(sql).fetchall()


def benchmark_one(con: duckdb.DuckDBPyConnection, sql: str, repeats: int) -> list[float]:
    """Ejecuta la consulta varias veces y devuelve los tiempos en ms."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        run_query(con, sql)
        dt = (time.perf_counter() - t0) * 1000  # ms
        times.append(dt)
    return times


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Parquet vs DuckDB table")
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS,
                        help=f"Repeticiones por consulta (default {DEFAULT_REPEATS})")
    args = parser.parse_args()

    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for vol_label, glob_pattern in VOLUMENES:
        print(f"\n{'='*70}")
        print(f"VOLUMEN: {vol_label}")
        print(f"  glob: {glob_pattern}")
        print(f"{'='*70}")

        where, and_where, pickup_expr = _where_for_volume(vol_label)

        # ── Conexion Parquet (en memoria, sin DB) ──
        con_mem = duckdb.connect()

        # ── Conexion tabla materializada ──
        if not Path(DB_PATH).exists():
            print(f"  ERROR: {DB_PATH} no existe. Ejecute primero build_duckdb.py")
            return
        con_db = duckdb.connect(DB_PATH, read_only=True)

        for q_name, sql_pq_template, sql_tbl_template in QUERIES:
            sql_pq = sql_pq_template.format(glob=glob_pattern, pickup_expr=pickup_expr)
            sql_tbl = sql_tbl_template.format(where=where, and_where=and_where)

            print(f"\n  {q_name}")

            # Parquet
            try:
                times_pq = benchmark_one(con_mem, sql_pq, args.repeats)
                med_pq = statistics.median(times_pq)
                print(f"    Parquet : mediana {med_pq:8.1f} ms  (tiempos: {[f'{t:.1f}' for t in times_pq]})")
            except Exception as e:
                print(f"    Parquet : ERROR — {e}")
                med_pq = None
                times_pq = []

            # Tabla DuckDB
            try:
                times_tbl = benchmark_one(con_db, sql_tbl, args.repeats)
                med_tbl = statistics.median(times_tbl)
                print(f"    Tabla   : mediana {med_tbl:8.1f} ms  (tiempos: {[f'{t:.1f}' for t in times_tbl]})")
            except Exception as e:
                print(f"    Tabla   : ERROR — {e}")
                med_tbl = None
                times_tbl = []

            if med_pq and med_tbl:
                speedup = med_pq / med_tbl
                print(f"    Speedup : {speedup:.2f}x")

            rows.append({
                "volumen": vol_label,
                "consulta": q_name,
                "mediana_parquet_ms": f"{med_pq:.1f}" if med_pq else "ERROR",
                "mediana_tabla_ms": f"{med_tbl:.1f}" if med_tbl else "ERROR",
                "speedup": f"{med_pq / med_tbl:.2f}" if (med_pq and med_tbl) else "N/A",
                "repeticiones": args.repeats,
            })

        con_mem.close()
        con_db.close()

    # ── Guardar CSV ─────────────────────────────────────────────────
    fieldnames = ["volumen", "consulta", "mediana_parquet_ms", "mediana_tabla_ms",
                  "speedup", "repeticiones"]
    with RESULTS_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'='*70}")
    print(f"Resultados guardados en: {RESULTS_CSV}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
