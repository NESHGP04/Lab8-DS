# Discusión – Persona A (Ejercicio 9: 9.5, 9.6 y 9.7)

## 9.5 ¿Qué características del sistema permiten incorporar nuevos datos con cambios mínimos?
- **Parametrización:** `--years` evita editar código; pasar de 2026 a 2024-2026 fue solo cambiar el argumento.
- **Convención de rutas** `data/raw/<tipo>/<año>/<nombre-original>.parquet` y consultas con *globs*: DuckDB
  descubre los archivos nuevos sin cambios en el SQL.
- **Idempotencia:** la descarga compara tamaño local y remoto; lo completo no se vuelve a bajar, lo truncado sí.
- **Descubrimiento en el servidor:** no se asumen meses; los que la TLC publique después se incorporan al volver a ejecutar.
- Nombres originales de la TLC: se conserva la trazabilidad con la fuente.

## 9.6 ¿Qué parte del proceso debería automatizarse en un sistema de producción?
1. **Ingesta programada** (cron/Airflow/GitHub Actions) del script de descarga: cada mes sale un archivo nuevo.
2. **Verificación automática** (`verify_data.py`) con alerta si falta un mes, el tamaño no coincide o el Parquet no abre.
3. **Reconstrucción de la base materializada** (`taxis.duckdb`) solo con los meses nuevos, y reporte de calidad de datos.
4. **Actualización del tablero** y pruebas de que las consultas siguen funcionando tras cada ingesta.
5. **Construcción de imágenes** y despliegue del ambiente en CI, con versiones fijadas.
6. Monitoreo de espacio en disco y registro (*log*) de cada ejecución.

## 9.7 ¿Qué decisiones de diseño fueron importantes para mantener el proyecto reproducible?
- **Docker + Docker Compose** con versiones exactas (`requirements.txt`, imagen base fija, DuckDB alineado con el driver de Metabase).
- **Datos fuera de git** (`.gitignore`) y **receta versionada** (script de descarga) en lugar de copias de los datos.
- **Descarga atómica** (`.part` + renombre) y reintentos: nunca quedan archivos a medias.
- **Verificación independiente** (`verify_data.py`) que evidencia que el conjunto es completo.
- **Rutas relativas** y volúmenes montados (`./data` → `/workspace/data`): el mismo código corre en el contenedor y en el host.
- **SQL y decisiones documentadas** en `sql/` y `docs/`, e historial de commits descriptivo.
