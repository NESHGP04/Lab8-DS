# Ambiente de trabajo (Ejercicio 1)

## 1.1 Fork
El trabajo se entrega sobre un fork de <https://github.com/menene/duckdb>. El remoto `upstream`
apunta al repositorio del docente (para recibir correcciones) y `origin` al repositorio del equipo.

## 1.2 Levantar el ambiente
```bash
docker compose up -d --build     # primera vez: ~5-10 min, descarga imágenes (~3 GB)
docker compose ps
```
`docker-compose.yml` define dos servicios:

| Servicio | Contenedor | URL | Para qué sirve |
|---|---|---|---|
| `lab` | `lab8-lab` | <http://localhost:8888> | JupyterLab con Python 3.11, DuckDB, pandas, pyarrow, matplotlib |
| `metabase` | `lab8-metabase` | <http://localhost:3000> | Metabase con el driver de DuckDB (tablero del Ej. 7) |

## 1.3 Verificación realizada
| Comprobación | Resultado |
|---|---|
| `docker compose ps` | `lab8-lab` y `lab8-metabase` en estado *Up* |
| `GET http://localhost:8888/api` (JupyterLab) | HTTP 200 |
| `GET http://localhost:3000/api/health` (Metabase) | HTTP 200, `{"status":"ok"}` |
| `import duckdb` dentro de `lab8-lab` y consulta a `/workspace/data/raw/*/*/*.parquet` | funciona (DuckDB 1.5.5) |
| Plugin de Metabase | `/home/metabase/plugins/duckdb.metabase-driver.jar` presente |

Salida real de estas comprobaciones: [evidencia/00_ambiente_servicios.txt](evidencia/00_ambiente_servicios.txt).

## 1.4 Herramientas disponibles
Contenedor `lab8-lab` (imagen `python:3.11.14-slim`, `requirements.txt`):
Python 3.11.14 · duckdb 1.5.5 · jupyterlab 4.6.4 · pandas 3.0.6 · pyarrow 25.0.1 · matplotlib 3.11.2 · requests 2.34.2 · curl.

Contenedor `lab8-metabase` (Debian jammy): OpenJDK 21 · Metabase v0.63.19 · driver DuckDB 1.5.5.0.

> La versión de `duckdb` en `requirements.txt` debe coincidir con la del driver de Metabase
> (ambas 1.5.5), porque ambos leen el mismo archivo `.duckdb`.

## Propósito de cada directorio
| Directorio | Propósito |
|---|---|
| `data/raw/` | Datos originales descargados, sin modificar (`<tipo>/<año>/*.parquet`, `zonas/`). Fuera de git. |
| `data/processed/` | Datos derivados, p. ej. la base materializada `taxis.duckdb` (Ej. 6). Fuera de git. |
| `notebooks/` | Notebooks de exploración, análisis, benchmark e indicadores. |
| `scripts/` | Código reutilizable: descarga, verificación, benchmark. |
| `sql/` | Consultas SQL versionadas, una por archivo, separadas por tema. |
| `docs/` | Documentación de consultas, decisiones y discusión. |
| `dashboard/` | Evidencia del tablero (capturas/exportes). |
| `Dockerfile`, `metabase.Dockerfile`, `docker-compose.yml` | Definición del ambiente reproducible. |

## 1.6 ¿Por qué un ambiente reproducible?
En un análisis de datos el resultado depende del código, de los **datos** y de las **versiones**
de las herramientas (DuckDB, pandas, pyarrow cambian tipos y comportamiento entre versiones).
Con Docker, versiones fijadas y un script de descarga, cualquier integrante —o el docente— obtiene
el mismo entorno con dos comandos, sin "en mi máquina funciona". Además: (1) los resultados se pueden
auditar y repetir, (2) se evita contaminar el Python del sistema, (3) el equipo se incorpora sin
instalar nada a mano, y (4) el mismo ambiente sirve en producción o en CI.
Los datos no se versionan (pesan GB): lo que se versiona es la *receta* para obtenerlos.
