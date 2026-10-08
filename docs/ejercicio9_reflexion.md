# Ejercicio 9: Discusión y Reflexión Final

Con base en el trabajo realizado a lo largo del laboratorio, se presentan las siguientes conclusiones:

### 9.1. ¿Qué características de DuckDB resultaron más útiles durante el laboratorio?

Su capacidad para leer directamente múltiples archivos utilizando comodines read*parquet('*/\_.parquet'), su integración nativa con Python y su velocidad analítica sin necesidad de configurar un servidor pesado.

### 9.2. ¿Qué ventajas y limitaciones encontró al consultar directamente archivos Parquet?

**Ventajas:** Ahorro total de espacio en disco (no hay duplicidad de datos) y acceso a la fuente original sin pasos intermedios.
**Limitaciones:** Rendimiento deficiente en consultas complejas (JOINs o funciones de agregación globales) y la dificultad lidiar con esquemas que cambian con los años (como el nombre de las columnas en taxis amarillos vs verdes).

### 9.3. ¿Qué ventajas y limitaciones observó al utilizar tablas materializadas en DuckDB?

**Ventajas:** Unificación y limpieza del esquema, y una velocidad drásticamente superior al renderizar tableros en herramientas de BI como Metabase.
**Limitaciones:** El almacenamiento se duplica, ya que se mantienen los archivos crudos Parquet y además se genera el archivo .duckdb (que llegó a pesar 2.5 GB).

### 9.4. ¿Qué ventajas ofrece este flujo de trabajo frente a cargar todos los datos utilizando una herramienta como Pandas?

Pandas intenta cargar todos los datos en la memoria RAM. Procesar 121 millones de filas colapsaría la memoria de casi cualquier computadora personal. DuckDB utiliza ejecución _Out-of-Core_, procesando los datos directamente desde el disco de forma eficiente sin agotar la RAM.

### 9.5. ¿Qué características del sistema desarrollado permiten incorporar nuevos datos con cambios mínimos?

El uso de rutas dinámicas (wildcards) y expresiones regulares regexp_extract en el script build_duckdb.py. Esto hace que el código sea agnóstico al tiempo; al descargar un nuevo año, el script lo absorbe automáticamente sin modificar ni una sola línea de código.

### 9.6. ¿Qué parte del proceso considera que debería automatizarse en un sistema de producción?

La ejecución del script de descarga mensual de datos (usando una herramienta como Airflow o un simple Cronjob) y la ingesta incremental (solo agregar el mes nuevo a DuckDB en lugar de reconstruir toda la tabla desde cero).

### 9.7. ¿Qué decisiones de diseño fueron importantes para mantener el proyecto reproducible?

El uso de Docker Compose para encapsular el entorno de trabajo (Base de Datos + Metabase + Python) y la estricta organización del proyecto por directorios funcionales data/raw, scripts/, sql/. Esto garantiza que cualquier persona pueda replicar el laboratorio en otra máquina.

### 9.8. ¿Qué aprendió sobre el manejo de datos que no habría sido evidente trabajando únicamente con conjuntos de datos pequeños?

Que la lectura de datos crudos tiene un techo físico muy rápido. Aprendimos la importancia vital de tener una capa de procesamiento (DuckDB), ya que operaciones que en bases pequeñas tardan milisegundos (como un simple COUNT o agrupar por mes), en Big Data pueden tardar minutos si no se modelan o materializan correctamente.
