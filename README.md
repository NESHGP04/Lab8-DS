# Lab 8 - DuckDB

Repositorio base del laboratorio 8 del curso **CC3084 - Data Science**
(Universidad del Valle de Guatemala, Ciclo 2, 2026).

Este es el repositorio **proporcionado por el docente**. Contiene la estructura
del proyecto, el ambiente de ejecucion basado en Docker y un script que descarga
los datos de **2026**. Todo lo demas debe ser construido por cada equipo.

## Trabajo con fork

El laboratorio se desarrolla y se entrega sobre un **fork** de este repositorio.
No se trabaja directamente sobre el repositorio del docente.

1. Realice un fork de este repositorio:
   <https://github.com/menene/duckdb>

2. Clone **su propio fork** (no el del docente):

   ```bash
   git clone https://github.com/<su-usuario>/duckdb.git
   cd duckdb
   ```

3. Opcional, para recibir correcciones publicadas por el docente:

   ```bash
   git remote add upstream https://github.com/menene/duckdb.git
   git fetch upstream
   ```

Realice commits frecuentes y descriptivos: el historial del repositorio es parte
de la evaluacion. **La entrega del laboratorio es la URL de su fork.**

## Estructura

```text
duckdb/
|
+-- data/
|   +-- raw/
|   +-- processed/
|
+-- notebooks/
|
+-- scripts/
|
+-- sql/
|
+-- docs/
|
+-- Dockerfile
+-- metabase.Dockerfile
+-- docker-compose.yml
+-- README.md
```

## Requisitos

- Docker, con Docker Compose
- Git

La primera construccion del ambiente descarga varios cientos de MB y puede
tardar algunos minutos.

Considere el espacio en disco: las imagenes de Docker ocupan unos 3 GB y los
datos de los tres anios del laboratorio superan 1.5 GB, a los que se suma la
base materializada del Ejercicio 6. Se recomienda tener al menos 10 GB libres.

## Datos

El repositorio incluye `scripts/download_data.py`, que descarga los archivos de
2026 publicados por la TLC (`--help` muestra las opciones disponibles). Los
archivos se guardan en `data/raw/<tipo>/<anio>/`.

La TLC publica cada mes con varias semanas de atraso, por lo que los ultimos
meses de 2026 todavia no existen. El script consulta al servidor que meses estan
publicados, de modo que vuelve a ejecutarse sin problema conforme aparezcan
nuevos archivos.

Los datos descargados **no deben incluirse en el repositorio Git**. El archivo
`.gitignore` ya esta configurado para evitarlo.

Fuente de datos: NYC TLC Trip Record Data
<https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>

Dentro de los contenedores, la carpeta `data/` del proyecto esta montada en
`/workspace/data`. Esa es la ruta que deben usar las herramientas que corren
dentro del ambiente, no la ruta de su computadora.

> **Nota sobre DuckDB:** un archivo `.duckdb` admite un solo proceso con permiso
> de escritura a la vez. Si conecta una herramienta externa a su base de datos,
> use el modo de solo lectura (`read_only`) en esa conexion; de lo contrario los
> demas procesos no podran abrir el archivo.

## Material a entregar

Al finalizar, su fork debe contener:

- el codigo fuente modificado y los scripts de descarga;
- las consultas SQL desarrolladas;
- el notebook o notebooks utilizados;
- la documentacion de las consultas;
- los scripts utilizados para los benchmarks;
- el codigo de los indicadores y visualizaciones;
- el tablero o la evidencia del tablero desarrollado;
- este `README.md`, completado segun la siguiente seccion.

Los archivos de datos descargados **no** deben incluirse.

---

# Documentacion del equipo

Las siguientes secciones deben ser completadas por cada equipo. El README final
debe permitir que una persona que no participo en el desarrollo pueda levantar el
ambiente, descargar los datos, ejecutar el analisis, reproducir los benchmarks y
generar los resultados principales.

## Como levantar el ambiente

Requisitos: Docker (con Docker Compose) y Git. Ver [docs/ambiente.md](docs/ambiente.md) para el detalle y la verificacion.

```bash
git clone https://github.com/<su-usuario>/<su-fork>.git
cd <su-fork>
docker compose up -d --build     # la primera vez tarda varios minutos (~3 GB de imagenes)
docker compose ps                # lab8-lab y lab8-metabase deben estar "Up"
```

| Servicio | URL | Verificacion |
|---|---|---|
| JupyterLab (sin token) | <http://localhost:8888> | `curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/api` -> `200` |
| Metabase | <http://localhost:3000> | `curl -s http://localhost:3000/api/health` -> `{"status":"ok"}` (tarda ~1 min en arrancar) |

Para apagar: `docker compose down`.

## Como descargar los datos

Los datos **no** estan en el repositorio; se obtienen con `scripts/download_data.py` (detalle de los
cambios y de la verificacion en [docs/descarga.md](docs/descarga.md)). Se puede ejecutar dentro del
contenedor (no requiere nada en su maquina) o en local con `pip install requests duckdb`:

```bash
# dentro del contenedor (recomendado)
docker exec -it lab8-lab python scripts/download_data.py --years 2024 2025 2026

# opciones
python scripts/download_data.py --years 2026                # solo 2026 (conjunto inicial, Ej. 2)
python scripts/download_data.py --years 2024 2026           # agrega 2024 (Ej. 5)
python scripts/download_data.py --years 2024 2025 2026      # conjunto completo (Ej. 8)
python scripts/download_data.py --taxi yellow --years 2025  # un solo tipo
python scripts/download_data.py --years 2025 --dry-run      # muestra el plan sin descargar
```

- Se guardan en `data/raw/<yellow|green>/<anio>/*.parquet` y `data/raw/zonas/taxi_zone_lookup.csv`.
- Es **idempotente**: no vuelve a descargar archivos completos (compara tamano local vs. servidor) y se puede
  ejecutar de nuevo cuando la TLC publique nuevos meses.
- El conjunto completo 2024-2026 son 64 archivos, ~121 millones de filas y ~2.0 GB.
- Verificar completitud e integridad:

```bash
docker exec -it lab8-lab python scripts/verify_data.py --years 2024 2025 2026
```

## Como ejecutar el analisis

> Pendiente: lo completan las Personas B y C (ver [docs/DIVISION_TAREAS.md](docs/DIVISION_TAREAS.md)).

Abrir <http://localhost:8888> y ejecutar los notebooks de `notebooks/` en orden
(`01_exploracion`, `02_eda`, `03_benchmark`, `04_indicadores`). Las consultas SQL estan en `sql/` y su
documentacion en `docs/`. Todas leen los datos con el patron `/workspace/data/raw/*/*/*.parquet`.

## Como reproducir los benchmarks

> Pendiente (Persona C, Ejercicio 6): `scripts/build_duckdb.py` y `scripts/benchmark.py`.

## Como generar los resultados principales

> Pendiente (Persona C, Ejercicios 7 y 8): tablero en Metabase (<http://localhost:3000>) y evidencia en `dashboard/`.
> Nota: Metabase debe abrir `data/processed/taxis.duckdb` en modo de solo lectura (`read_only`).
