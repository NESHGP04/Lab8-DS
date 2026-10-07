#!/usr/bin/env python3
"""Descarga los archivos Parquet del NYC TLC Trip Record Data.

Descarga los registros de viajes de taxis amarillos (yellow) y verdes (green)
para uno o varios anios, mas la tabla de zonas (taxi_zone_lookup.csv).

Fuente oficial de los datos:
    https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Uso:
    python scripts/download_data.py                       # amarillos y verdes, 2026
    python scripts/download_data.py --years 2024 2026     # incorpora 2024 (Ej. 5)
    python scripts/download_data.py --years 2024 2025 2026  # conjunto completo (Ej. 8)
    python scripts/download_data.py --taxi yellow --years 2025
    python scripts/download_data.py --years 2025 --dry-run  # solo muestra el plan

Los archivos se guardan en:
    data/raw/<tipo>/<anio>/<nombre-original>.parquet
    data/raw/zonas/taxi_zone_lookup.csv

Comportamiento:
  - La TLC publica cada mes con varias semanas de atraso, por lo que no todos
    los meses del anio en curso existen todavia. El script consulta al servidor
    que meses estan publicados en lugar de suponerlos.
  - Un archivo que ya existe localmente no se vuelve a descargar. Se considera
    "existente" si su tamanio coincide con el Content-Length del servidor; un
    archivo truncado o corrupto se vuelve a bajar.
  - La descarga se hace sobre un nombre temporal y solo se renombra al
    terminar, de modo que una interrupcion no deja archivos .parquet a medias.
  - Agregar un anio nuevo no requiere tocar el codigo: basta con pasarlo en
    --years. Los anios ya descargados se conservan.
"""

import argparse
import sys
from pathlib import Path

import requests

ANIO_ACTUAL_POR_DEFECTO = (2026,)
TIPOS_TAXI = ("yellow", "green")
URL_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"
URL_ZONAS = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
DIR_DESTINO = Path("data/raw")
RUTA_ZONAS = DIR_DESTINO / "zonas" / "taxi_zone_lookup.csv"

TIEMPO_ESPERA = 60          # segundos por peticion
INTENTOS = 3                # intentos por archivo antes de darse por vencido
BLOQUE = 1024 * 1024        # 1 MiB por bloque de descarga
SUFIJO_TEMPORAL = ".part"


def construir_nombre(tipo: str, anio: int, mes: int) -> str:
    """Nombre del archivo publicado por la TLC, p. ej. yellow_tripdata_2026-01.parquet."""
    return f"{tipo}_tripdata_{anio}-{mes:02d}.parquet"


def construir_url(tipo: str, anio: int, mes: int) -> str:
    """URL completa del archivo Parquet mensual."""
    return f"{URL_BASE}/{construir_nombre(tipo, anio, mes)}"


def ruta_destino(tipo: str, anio: int, mes: int) -> Path:
    """Ruta local donde se guarda el archivo."""
    return DIR_DESTINO / tipo / str(anio) / construir_nombre(tipo, anio, mes)


def tamanio_remoto(url: str) -> int | None:
    """Tamanio (bytes) del archivo en el servidor, o None si no esta publicado.

    Usa HEAD, sin descargar el contenido. Si el servidor responde pero no informa
    Content-Length, devuelve 0 (publicado, tamanio desconocido).
    """
    try:
        respuesta = requests.head(url, timeout=TIEMPO_ESPERA, allow_redirects=True)
    except requests.RequestException:
        return None
    if not respuesta.ok:
        return None
    return int(respuesta.headers.get("Content-Length", 0))


def formato_tamanio(n: float) -> str:
    for unidad in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unidad == "GiB":
            return f"{n:.1f} {unidad}"
        n /= 1024
    return f"{n:.1f} GiB"


def descargar_archivo(url: str, destino: Path) -> int:
    """Descarga `url` en `destino`. Devuelve la cantidad de bytes escritos."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_name(destino.name + SUFIJO_TEMPORAL)

    ultimo_error = None
    for intento in range(1, INTENTOS + 1):
        try:
            with requests.get(url, stream=True, timeout=TIEMPO_ESPERA) as respuesta:
                respuesta.raise_for_status()
                escritos = 0
                with temporal.open("wb") as archivo:
                    for bloque in respuesta.iter_content(chunk_size=BLOQUE):
                        if bloque:
                            archivo.write(bloque)
                            escritos += len(bloque)
            if escritos == 0:
                raise requests.RequestException("el servidor devolvio un archivo vacio")
            temporal.replace(destino)
            return escritos
        except requests.RequestException as error:
            ultimo_error = error
            temporal.unlink(missing_ok=True)
            if intento < INTENTOS:
                print(f"      intento {intento}/{INTENTOS} fallido ({error}); reintentando")

    raise requests.RequestException(f"no se pudo descargar {url}: {ultimo_error}")


def ya_existe(destino: Path, tamanio_servidor: int) -> bool:
    """True si el archivo local esta completo (existe y coincide con el servidor)."""
    if not destino.exists():
        return False
    local = destino.stat().st_size
    if local == 0:
        return False
    # tamanio_servidor == 0 significa "desconocido": basta con que no este vacio.
    return tamanio_servidor == 0 or local == tamanio_servidor


def descargar(tipo: str, anio: int, dry_run: bool) -> dict:
    """Descarga todos los meses publicados de un tipo de taxi para un anio."""
    print(f"\n=== {tipo.upper()} {anio} ===")
    resumen = {"descargados": 0, "omitidos": 0, "no_publicados": [], "fallidos": []}

    for mes in range(1, 13):
        etiqueta = f"{anio}-{mes:02d}"
        destino = ruta_destino(tipo, anio, mes)
        url = construir_url(tipo, anio, mes)

        tamanio = tamanio_remoto(url)
        if tamanio is None:
            print(f"  {etiqueta}  aun no publicado por la TLC")
            resumen["no_publicados"].append(etiqueta)
            continue

        if ya_existe(destino, tamanio):
            print(f"  {etiqueta}  ya existe, se omite")
            resumen["omitidos"] += 1
            continue

        if dry_run:
            print(f"  {etiqueta}  se descargaria ({formato_tamanio(tamanio)})")
            continue

        print(f"  {etiqueta}  descargando...")
        try:
            escritos = descargar_archivo(url, destino)
        except requests.RequestException as error:
            print(f"  {etiqueta}  ERROR: {error}")
            resumen["fallidos"].append(etiqueta)
        else:
            print(f"  {etiqueta}  listo ({formato_tamanio(escritos)}) -> {destino}")
            resumen["descargados"] += 1

    return resumen


def descargar_zonas(dry_run: bool) -> bool:
    """Descarga la tabla de zonas (CSV pequeno) si todavia no existe."""
    print("\n=== ZONAS ===")
    if RUTA_ZONAS.exists() and RUTA_ZONAS.stat().st_size > 0:
        print("  taxi_zone_lookup.csv  ya existe, se omite")
        return True
    if dry_run:
        print("  taxi_zone_lookup.csv  se descargaria")
        return True
    try:
        descargar_archivo(URL_ZONAS, RUTA_ZONAS)
    except requests.RequestException as error:
        print(f"  taxi_zone_lookup.csv  ERROR: {error}")
        return False
    print(f"  taxi_zone_lookup.csv  listo -> {RUTA_ZONAS}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Descarga los datos de taxis (yellow/green) del NYC TLC."
    )
    parser.add_argument(
        "--taxi", choices=(*TIPOS_TAXI, "all"), default="all",
        help="tipo de taxi a descargar (por defecto: all)",
    )
    parser.add_argument(
        "--years", type=int, nargs="+", default=list(ANIO_ACTUAL_POR_DEFECTO),
        metavar="ANIO",
        help="anios a descargar, p. ej. --years 2024 2025 2026 (por defecto: 2026)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="solo muestra que se descargaria, sin escribir archivos",
    )
    parser.add_argument(
        "--skip-zones", action="store_true",
        help="no descarga taxi_zone_lookup.csv",
    )
    argumentos = parser.parse_args()

    tipos = TIPOS_TAXI if argumentos.taxi == "all" else (argumentos.taxi,)
    anios = sorted(set(argumentos.years))

    total = {"descargados": 0, "omitidos": 0, "no_publicados": [], "fallidos": []}
    for anio in anios:
        for tipo in tipos:
            resumen = descargar(tipo, anio, argumentos.dry_run)
            total["descargados"] += resumen["descargados"]
            total["omitidos"] += resumen["omitidos"]
            total["no_publicados"] += [f"{tipo} {m}" for m in resumen["no_publicados"]]
            total["fallidos"] += [f"{tipo} {m}" for m in resumen["fallidos"]]

    zonas_ok = True if argumentos.skip_zones else descargar_zonas(argumentos.dry_run)

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"  anios         : {', '.join(map(str, anios))}")
    print(f"  descargados   : {total['descargados']}")
    print(f"  ya existian   : {total['omitidos']}")
    print(f"  no publicados : {len(total['no_publicados'])}")
    if total["no_publicados"]:
        print(f"      {', '.join(total['no_publicados'])}")
    print(f"  fallidos      : {len(total['fallidos'])}")
    if total["fallidos"]:
        print(f"      {', '.join(total['fallidos'])}")
    print("=" * 60)

    return 1 if total["fallidos"] or not zonas_ok else 0


if __name__ == "__main__":
    sys.exit(main())
