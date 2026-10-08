#!/usr/bin/env python3
"""Construye (o reconstruye) la base de datos DuckDB materializada.

Lee todos los Parquets de data/raw/ y los materializa en una tabla 'viajes'
dentro de data/processed/taxis.duckdb.  Tambien carga la tabla de zonas.

La tabla se recrea cada vez que se ejecuta el script, para garantizar que
refleje exactamente los archivos disponibles en disco.

Uso:
    python scripts/build_duckdb.py
"""

import time
from pathlib import Path

import duckdb

PARQUET_GLOB = "data/raw/*/*/*.parquet"
ZONAS_CSV = "data/raw/zonas/taxi_zone_lookup.csv"
DB_PATH = Path("data/processed/taxis.duckdb")


def build(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Eliminar DB anterior para reconstruir limpio
    if db_path.exists():
        db_path.unlink()
        print(f"  Base anterior eliminada: {db_path}")

    con = duckdb.connect(str(db_path))

    # ── Tabla viajes ────────────────────────────────────────────────
    print("\n=== Construyendo tabla 'viajes' ===")
    t0 = time.perf_counter()

    con.execute(f"""
        CREATE TABLE viajes AS
        SELECT
            regexp_extract(filename, '(yellow|green)_tripdata_', 1)          AS tipo,
            TRY_CAST(regexp_extract(filename, '(20[0-9]{{2}})-[0-9]{{2}}\\.parquet$', 1) AS INTEGER) AS anio_archivo,
            COALESCE(
                TRY_CAST(tpep_pickup_datetime  AS TIMESTAMP),
                TRY_CAST(lpep_pickup_datetime  AS TIMESTAMP)
            ) AS inicio,
            COALESCE(
                TRY_CAST(tpep_dropoff_datetime AS TIMESTAMP),
                TRY_CAST(lpep_dropoff_datetime AS TIMESTAMP)
            ) AS fin,
            TRY_CAST(passenger_count AS DOUBLE)  AS pasajeros,
            TRY_CAST(trip_distance   AS DOUBLE)  AS distancia_millas,
            TRY_CAST(fare_amount     AS DOUBLE)  AS tarifa,
            TRY_CAST(total_amount    AS DOUBLE)  AS total,
            TRY_CAST(tip_amount      AS DOUBLE)  AS propina,
            TRY_CAST(payment_type    AS INTEGER)  AS tipo_pago,
            TRY_CAST(PULocationID    AS INTEGER)  AS zona_recogida,
            TRY_CAST(DOLocationID    AS INTEGER)  AS zona_destino
        FROM read_parquet('{PARQUET_GLOB}',
                          union_by_name = true,
                          filename = true,
                          hive_partitioning = false)
    """)

    dt = time.perf_counter() - t0
    filas = con.execute("SELECT count(*) FROM viajes").fetchone()[0]
    print(f"  {filas:,} filas insertadas en {dt:.1f}s")

    # ── Tabla zonas ─────────────────────────────────────────────────
    print("\n=== Construyendo tabla 'zonas' ===")
    if Path(ZONAS_CSV).exists():
        con.execute(f"""
            CREATE TABLE zonas AS
            SELECT * FROM read_csv_auto('{ZONAS_CSV}')
        """)
        filas_z = con.execute("SELECT count(*) FROM zonas").fetchone()[0]
        print(f"  {filas_z} zonas cargadas")
    else:
        print(f"  ADVERTENCIA: {ZONAS_CSV} no encontrado, tabla zonas no creada")

    # ── Resumen ─────────────────────────────────────────────────────
    print("\n=== Resumen de la base ===")
    tablas = con.execute("SHOW TABLES").fetchall()
    for (tabla,) in tablas:
        n = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
        print(f"  {tabla}: {n:,} filas")

    tam = db_path.stat().st_size / (1024 * 1024)
    print(f"\n  Archivo: {db_path}  ({tam:.1f} MiB)")

    con.close()
    
    # ── Validación de la ingestión del 2025 ─────────────────────────
    con2 = duckdb.connect(str(db_path), read_only=True)
    anios = con2.execute("SELECT DISTINCT anio_archivo FROM viajes ORDER BY 1").fetchall()
    print("\nAños detectados exitosamente en la base de datos:")
    for a in anios:
        print(f" - {a[0]}")
    con2.close()
    
    print("\nListo.")

if __name__ == "__main__":
    build()
