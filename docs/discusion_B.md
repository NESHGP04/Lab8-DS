# Discusión — Persona B

## 9.1 Características de DuckDB más útiles

`read_parquet` permite aplicar SQL directamente al glob de archivos, `parquet_file_metadata` ofrece recuentos sin recorrer las columnas de viajes, `DESCRIBE` muestra los tipos inferidos y `union_by_name` concilia columnas diferentes entre años y servicios. Las vistas temporales permiten normalizar marcas de tiempo y nombres de columnas dentro de la sesión. Para evaluar cuál operación dominó el tiempo de ejecución en este equipo se necesita medirla; aquí no se presentan benchmarks.

## 9.2 Ventajas y limitaciones de Parquet directo

Al leer desde el origen se evita duplicar todos los datos en una tabla. Parquet almacena columnas y metadatos por grupos de filas, lo que permite a DuckDB leer columnas necesarias y en algunos filtros descartar grupos. Un glob admite archivos nuevos al reejecutar consultas sin modificar SQL si mantienen la ruta y un esquema compatible. La lectura repetida y el descubrimiento del esquema de muchos archivos pueden costar tiempo e I/O. Cambios incompatibles de tipo, archivos dañados o meses ausentes requieren validación explícita. Un glob no prueba completitud. En la ejecución adjunta, las seis agregaciones de `count(*)` coinciden con los footers; esto valida los archivos presentes, pero no prueba que se descargaran todos los publicados.

## 9.4 Frente a cargar todo con Pandas

Las agregaciones se ejecutan dentro del motor sin materializar todas las filas como un DataFrame; se puede devolver a Python una tabla pequeña de resultados en vez de cargar los viajes completos en RAM. La diferencia real de velocidad depende de archivos, filtros, almacenamiento y memoria; sin medición local no se le asigna un factor de mejora. Pandas sigue siendo útil para visualizar y trabajar con resultados agregados.

## 9.8 Qué revela un conjunto grande

A escala de muchos archivos y años aparecen diferencias de esquema, meses desiguales, registros fechados fuera del año nominal, colas largas y el costo de volver a consultar o inspeccionar footers. Una muestra pequeña puede omitir casos raros y dar una impresión engañosa de las proporciones. Los resultados por servicio y año y sus denominadores permiten detectar si un hallazgo se concentra en una cohorte. En esta ejecución, `count(*)` confirmó los 121.184.384 registros informados por los footers de 64 archivos. La validación mostró fechas tan tempranas como 2001 dentro de archivos nominalmente de 2026, lo cual exige filtrar por año efectivo de inicio antes de comparar actividad mensual.

## Alcance

Las consultas detectan asociaciones descriptivas; no identifican causas ni justifican extrapolación a meses ausentes. El código `payment_type` requiere cotejarse con los diccionarios del periodo antes de atribuir nombres a categorías. La consulta de propinas excluye valores negativos sólo al calcular la media, no del conteo de viajes.
