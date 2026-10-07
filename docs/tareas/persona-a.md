# Persona A — Infraestructura, datos y reproducibilidad

Rama: `persona-a/infra-datos` · Fase 1 (Pasaporte, 15 pts) completa + 10 pts incorporación incremental + 5 pts reproducibilidad.
Archivos propios: `scripts/download_data.py`, `scripts/verify_data.py`, `README.md`, `docs/ambiente.md`, `docs/descarga.md`, `docs/discusion_A.md`.

## Fase 1 — Pasaporte (entregar primero)
### Ejercicio 1 — Ambiente
- [ ] 1.1 Fork del repositorio del docente (`menene/duckdb`)
- [ ] 1.2 Clonar el fork y levantar con `docker compose up --build`
- [ ] 1.3 Verificar servicios: JupyterLab (`localhost:8888`) y Metabase (`localhost:3000`)
- [ ] 1.4 Listar herramientas disponibles dentro del ambiente (Python, duckdb, pandas, pyarrow, matplotlib, jupyterlab, Metabase + driver)
- [ ] 1.5 Documentar el procedimiento en el README ("Cómo levantar el ambiente")
- [ ] 1.6 Explicar por qué un ambiente reproducible importa (`docs/ambiente.md`)
- [ ] Explicar el propósito de cada directorio (`data/raw`, `data/processed`, `notebooks`, `scripts`, `sql`, `docs`)

### Ejercicio 2 — Sistema de descarga (2026)
- [ ] 2.1 Analizar el script base y listar qué se modifica
- [ ] 2.2 Descargar yellow + green 2026
- [ ] 2.3 Guardar en `data/raw/<tipo>/<año>/`
- [ ] 2.4 No re-descargar lo que ya existe
- [ ] 2.5 Ejecutar y verificar (`scripts/verify_data.py`)
- [ ] 2.6 Documentar cambios al script (`docs/descarga.md`)
- [ ] 2.7 Explicar cómo se determinó que el conjunto está completo

## Fase 2
### Ejercicio 5 (parte de datos)
- [ ] 5.1 `--years 2024 2026` incorpora 2024
- [ ] 5.2 / 5.3 / 5.4 Conservar 2026, no re-descargar, re-ejecutar
- [ ] 5.5 Verificar los archivos nuevos
- [ ] 5.9 Explicar qué decisiones de diseño permiten añadir datos sin tocar el análisis (globs + `--years`)

### Ejercicio 8 (parte de datos)
- [ ] 8.1 `--years 2024 2025 2026`
- [ ] 8.2 Verificar que lo ya descargado no se vuelve a bajar

### Ejercicio 9 (discusión)
- [ ] 9.5 ¿Qué permite incorporar nuevos datos con cambios mínimos?
- [ ] 9.6 ¿Qué automatizar en producción?
- [ ] 9.7 ¿Qué decisiones de diseño mantuvieron el proyecto reproducible?

### Cierre del repositorio
- [ ] README completo (5 secciones TODO) integrando los párrafos de B y C
- [ ] `.gitignore` sin datos; historial de commits claro

## Independencia
No necesita nada de B ni C. B y C usan `data/raw/*/*/*.parquet` y solo requieren que alguien ejecute el script (el de la base ya baja 2026).
