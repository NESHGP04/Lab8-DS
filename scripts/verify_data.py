#!/usr/bin/env python3
"""Verifica que los datos descargados estan completos y son legibles (Ej. 2.5 y 2.7).

Para cada tipo de taxi y anio pedido comprueba, con DuckDB y sin cargar los
datos en memoria:
  1. que exista el archivo de cada mes publicado por la TLC (HEAD al servidor);
  2. que el tamanio local coincida con el Content-Length del servidor;
  3. que el footer de Parquet sea legible (parquet_file_metadata) y tenga filas.

Uso:
    python scripts/verify_data.py                     # 2026
    python scripts/verify_data.py --years 2024 2025 2026
"""

import argparse
import sys

import duckdb

from download_data import (
    DIR_DESTINO, TIPOS_TAXI, construir_url, ruta_destino, tamanio_remoto,
)


def verificar(tipo: str, anio: int) -> list[str]:
    problemas: list[str] = []
    publicados = 0
    for mes in range(1, 13):
        etiqueta = f"{tipo} {anio}-{mes:02d}"
        remoto = tamanio_remoto(construir_url(tipo, anio, mes))
        destino = ruta_destino(tipo, anio, mes)
        if remoto is None:
            if destino.exists():
                problemas.append(f"{etiqueta}: existe local pero el servidor no lo lista")
            continue
        publicados += 1
        if not destino.exists():
            problemas.append(f"{etiqueta}: FALTA (publicado en el servidor)")
            continue
        local = destino.stat().st_size
        if remoto and local != remoto:
            problemas.append(f"{etiqueta}: tamanio local {local} != remoto {remoto}")
            continue
        try:
            filas = duckdb.sql(
                f"SELECT num_rows FROM parquet_file_metadata('{destino}')"
            ).fetchone()[0]
        except duckdb.Error as error:
            problemas.append(f"{etiqueta}: Parquet ilegible ({error})")
            continue
        if not filas:
            problemas.append(f"{etiqueta}: Parquet sin filas")
        else:
            print(f"  OK  {etiqueta}  {filas:>10,} filas")
    print(f"  -> {tipo} {anio}: {publicados} meses publicados por la TLC")
    return problemas


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica la completitud de los datos.")
    parser.add_argument("--years", type=int, nargs="+", default=[2026], metavar="ANIO")
    parser.add_argument("--taxi", choices=(*TIPOS_TAXI, "all"), default="all")
    args = parser.parse_args()

    tipos = TIPOS_TAXI if args.taxi == "all" else (args.taxi,)
    problemas: list[str] = []
    for anio in sorted(set(args.years)):
        for tipo in tipos:
            print(f"\n=== {tipo.upper()} {anio} ===")
            problemas += verificar(tipo, anio)

    print("\n" + "=" * 60)
    if problemas:
        print(f"PROBLEMAS ({len(problemas)}):")
        for p in problemas:
            print(f"  - {p}")
        return 1
    print(f"Datos completos en {DIR_DESTINO}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
