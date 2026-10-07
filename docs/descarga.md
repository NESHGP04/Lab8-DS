# Sistema de descarga (Ejercicios 2, 5 y 8)

Script: [`scripts/download_data.py`](../scripts/download_data.py) · Verificación: [`scripts/verify_data.py`](../scripts/verify_data.py)

## 2.1 Análisis del script base
El script del docente descargaba solo 2026, pero tenía límites para el resto del laboratorio:

| Observación | Consecuencia |
|---|---|
| `ANIO = 2026` fijo en el código | Para 2024 y 2025 habría que editar el código cada vez |
| "Ya existe" = archivo con tamaño > 0 | Un archivo truncado (corte de red, disco lleno) se daría por bueno |
| No descarga `taxi_zone_lookup.csv` | Las consultas con zonas (Ej. 4, 7) no tendrían la tabla |
| No hay modo de simulación ni verificación | No se puede comprobar completitud (2.7) sin descargar |

## 2.2–2.4 y 2.6 Cambios realizados
| Cambio | Motivo |
|---|---|
| `--years 2024 2025 2026` (por defecto `2026`) | Incorporar años (Ej. 5 y 8) sin tocar código |
| `construir_nombre/url/ruta_destino` reciben `anio` | El año deja de ser constante global |
| `tamanio_remoto()` con `HEAD` y `Content-Length` | Sabe qué meses están publicados **y** su tamaño real |
| `ya_existe()` compara tamaño local vs remoto | No re-descarga lo completo (2.4) y sí re-descarga lo truncado |
| `descargar_zonas()` → `data/raw/zonas/taxi_zone_lookup.csv` | Tabla de zonas para joins |
| `--dry-run` | Muestra el plan (archivos y MiB) sin escribir nada |
| `--skip-zones` | Omitir el CSV de zonas |
| Se mantienen: descarga a `.part` + renombre atómico, 3 reintentos, estructura `data/raw/<tipo>/<año>/` | Robustez y 2.3 |

## 2.5 / 5.4 / 8.1 Ejecuciones realizadas
| Ejecución | Comando | Descargados | Ya existían | No publicados | Fallidos |
|---|---|---|---|---|---|
| Ej. 2: solo 2026 | `--years 2026` | 16 | 0 | 8 | 0 |
| Ej. 2.4: repetida | `--years 2026` | 0 | 16 | 8 | 0 |
| Ej. 5: se agrega 2024 | `--years 2024 2026` | 24 | 16 | 8 | 0 |
| Ej. 8: se agrega 2025 | `--years 2024 2025 2026` | 24 | 40 | 8 | 0 |
| Ej. 8.2: repetida (también dentro del contenedor) | `--years 2024 2025 2026` | **0** | **64** | 8 | 0 |

Los 8 "no publicados" son septiembre–diciembre de 2026, que la TLC aún no publica (yellow y green).
Los archivos de 2026 se conservaron al agregar 2024 y 2025 (5.2): en cada corrida posterior aparecen como "ya existe".

## 2.7 ¿Cómo se determinó que el conjunto está completo?
`scripts/verify_data.py` comprueba, por cada tipo y año:
1. **Existencia:** cada mes que el servidor publica (HEAD) tiene su archivo local; ninguno falta.
2. **Integridad:** tamaño local = `Content-Length` del servidor.
3. **Legibilidad:** el *footer* Parquet se lee con DuckDB (`parquet_file_metadata`) y tiene filas > 0.

Resultado con 2024–2026: sin problemas. Inventario obtenido desde los metadatos Parquet:

| Tipo | Año | Archivos | Filas | Tamaño en disco |
|---|---|---|---|---|
| yellow | 2024 | 12 | 41 169 720 | 661 MB |
| yellow | 2025 | 12 | 48 722 602 | 865 MB |
| yellow | 2026 | 8 | 29 703 355 | 501 MB |
| green | 2024 | 12 | 660 218 | 15 MB |
| green | 2025 | 12 | 591 375 | 14 MB |
| green | 2026 | 8 | 337 114 | 7.9 MB |
| **Total** | | **64** | **121 184 384** | **≈ 2.0 GB** |

## 5.9 Diseño que permite incorporar datos sin modificar el análisis
- Las consultas leen con *globs* (`data/raw/*/*/*.parquet`), no con listas de archivos: un año nuevo
  entra solo con descargarlo.
- Estructura estable `data/raw/<tipo>/<año>/`: el año y el tipo se pueden derivar de la ruta (`filename`).
- La descarga es **idempotente** e **incremental**: se puede ejecutar cuantas veces se quiera.
- El script no asume meses: pregunta al servidor qué existe, por lo que corre igual conforme la TLC publica.
- Datos fuera de git y receta versionada.

## Evidencia (salida real de las ejecuciones)
Registros completos en [`docs/evidencia/`](evidencia/):

| Archivo | Contenido |
|---|---|
| [01_descarga_2026.log](evidencia/01_descarga_2026.log) | Ej. 2: primera descarga de 2026 (16 descargados) |
| [02_descarga_2026_repetida.log](evidencia/02_descarga_2026_repetida.log) | Ej. 2.4: repetida, 0 descargados / 16 existentes |
| [03_verificacion_2026.log](evidencia/03_verificacion_2026.log) | Ej. 2.5 y 2.7: verificación de 2026 |
| [04_descarga_2024_y_2026.log](evidencia/04_descarga_2024_y_2026.log) | Ej. 5: se agrega 2024, 2026 se conserva |
| [05_descarga_2024_2025_2026.log](evidencia/05_descarga_2024_2025_2026.log) | Ej. 8.1: se agrega 2025 |
| [06_descarga_repetida_2024_2025_2026.log](evidencia/06_descarga_repetida_2024_2025_2026.log) | Ej. 8.2: repetida, 0 descargados / 64 existentes |
| [07_verificacion_2024_2025_2026.log](evidencia/07_verificacion_2024_2025_2026.log) | Verificación final del conjunto completo |
