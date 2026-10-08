# Ejercicio 6: Benchmark — Parquet versus Tablas Materializadas en DuckDB

## Resultados del Benchmark

A continuación se presentan los resultados de ejecutar 5 consultas representativas sobre dos estrategias distintas: consultar directamente archivos Parquet y consultar una tabla materializada en DuckDB.

Los tiempos mostrados corresponden a la mediana de 5 repeticiones en milisegundos.

| Volumen de Datos                     | Consulta        | Mediana Parquet (ms) | Mediana Tabla (ms) | Speedup (Tabla vs Parquet)                |
| :----------------------------------- | :-------------- | :------------------- | :----------------- | :---------------------------------------- |
| **1 mes** (Ene 2024, 3M filas)       | Q1 Agregación   | 12.0                 | 30.6               | 0.39x (Parquet más rápido)                |
|                                      | Q2 Filtro       | 12.6                 | 30.4               | 0.41x (Parquet más rápido)                |
|                                      | Q3 Temporal     | 63.6                 | 37.4               | 1.70x (Tabla más rápida)                  |
|                                      | Q4 JOIN zonas   | 52.3                 | 33.0               | 1.58x (Tabla más rápida)                  |
|                                      | Q5 Top-N Window | 39.9                 | 30.7               | 1.30x (Tabla más rápida)                  |
| **3 meses** (Ene-Mar 2024, 9M filas) | Q1 Agregación   | 18.3                 | 42.3               | 0.43x (Parquet más rápido)                |
|                                      | Q2 Filtro       | 19.2                 | 31.9               | 0.60x (Parquet más rápido)                |
|                                      | Q3 Temporal     | 77.4                 | 69.2               | 1.12x (Tabla más rápida)                  |
|                                      | Q4 JOIN zonas   | 68.8                 | 58.5               | 1.18x (Tabla más rápida)                  |
|                                      | Q5 Top-N Window | 52.1                 | 45.6               | 1.14x (Tabla más rápida)                  |
| **1 año** (2024, 38M filas)          | Q1 Agregación   | 61.7                 | 79.8               | 0.77x (Parquet más rápido)                |
|                                      | Q2 Filtro       | 69.0                 | 33.6               | 2.06x (Tabla más rápida)                  |
|                                      | Q3 Temporal     | 263.3                | 177.9              | 1.48x (Tabla más rápida)                  |
|                                      | Q4 JOIN zonas   | 224.8                | 132.0              | 1.70x (Tabla más rápida)                  |
|                                      | Q5 Top-N Window | 159.6                | 74.3               | 2.15x (Tabla más rápida)                  |
| **Todo** (2024-2026, 72M filas)      | Q1 Agregación   | 107.8                | 114.5              | 0.94x (Empate/Parquet ligeramente rápido) |
|                                      | Q2 Filtro       | 112.9                | 55.2               | 2.04x (Tabla más rápida)                  |
|                                      | Q3 Temporal     | 505.4                | 302.7              | 1.67x (Tabla más rápida)                  |
|                                      | Q4 JOIN zonas   | 401.4                | 184.4              | 2.18x (Tabla más rápida)                  |
|                                      | Q5 Top-N Window | 305.1                | 100.6              | 3.03x (Tabla más rápida)                  |

---

## Análisis de las Diferencias (6.9)

A partir de los resultados observados, podemos identificar los siguientes patrones:

1. Para consultas donde se necesita escanear y agregar columnas enteras sin filtros complejos ni transformaciones en las fechas (como la Q1), leer directamente de Parquet fue igual o incluso más rápido que usar la tabla materializada, especialmente con volúmenes bajos de datos (1 a 3 meses). Esto se debe a la naturaleza columnar de Parquet y a los eficientes metadatos que DuckDB explota para saltar bloques no relevantes.

2. A medida que las consultas se vuelven más complejas (Q3 Temporal con date*trunc, Q4 con JOIN a la tabla de zonas, y Q5 con \_Window Functions* row_number()), la tabla materializada muestra una clara ventaja. En la Q5 con todo el volumen (Todo 2024+2026), la tabla materializada fue 3 veces más rápida (100.6 ms vs 305.1 ms). Esto indica que DuckDB puede optimizar y ejecutar mejor los planes de ejecución sobre su propio formato de almacenamiento interno cuando hay múltiples operaciones.

3. Con 1 mes o 3 meses de datos (3 a 9 millones de filas), las diferencias absolutas de tiempo son de escasos milisegundos; en la práctica el usuario no notaría la diferencia. Sin embargo, al escalar a 72 millones de filas (Todo), la diferencia en operaciones costosas como filtros y ordenamientos se vuelve muy significativa. Por ejemplo, en Q2 (Filtro) la tabla materializada se mantiene sorprendentemente constante en tiempo (~55 ms) mientras que Parquet sube a 113 ms, lo que sugiere el posible uso de optimizaciones de filtrado y metadata que DuckDB maneja nativamente mejor.

---

## ¿Cuándo usar Parquet directo y cuándo materializar? (6.10)

**Cuándo consultar directamente archivos Parquet:**

- **Fase de Exploración inicial:** Cuando se están conociendo los datos, revisando el esquema o extrayendo muestras. Ahorra el tiempo y el espacio en disco necesarios para importar y duplicar los datos.
- **Consultas tipo "Write-Once, Read-Rarely":** Para extraer reportes puntuales (agregaciones o conteos simples) sobre grandes archivos (Data Lakes), donde no justifica el overhead de importarlos a un RDBMS.
- **Limitaciones de Almacenamiento:** Si el disco no tiene el espacio suficiente para almacenar tanto el Parquet original como la base de datos DuckDB (nuestra DB pesa 1.5 GB adicional).

**Cuándo materializar una tabla en DuckDB:**

- **Consultas Repetitivas y Complejas:** Cuando el conjunto de datos será la base de un tablero analítico (como Metabase) o de reportes concurrentes recurrentes que requieran JOINs pesados, agrupaciones por fechas y funciones de ventana. Materializar mejora notablemente el "Speedup".
- **Mejorar el Rendimiento en Filtros:** Cuando los analistas buscarán constantemente "agujas en un pajar" (filtros específicos). DuckDB puede usar sus índices de zona/metadatos más rápidamente en su propio almacenamiento.
- **Tipos de Datos Consistentes y Limpieza:** Cuando los Parquets crudos tienen esquemas inconsistentes (por ejemplo, tipos de columnas que varían entre meses) que requieren COALESCE o conversiones constantes (como pasó con tpep_pickup_datetime y lpep_pickup_datetime). Una vez insertado en DuckDB en una tabla consolidada, el analista consulta la información ya limpiada sin lidiar con los errores de lectura de esquemas mutantes.
