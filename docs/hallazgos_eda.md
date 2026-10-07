# EDA de taxis amarillos y verdes

Estado: consultas preparadas, hallazgos pendientes de ejecutar sobre los archivos del fork. `notebooks/02_eda.ipynb` sustituirá estas secciones con tablas observadas.

La fuente de cada consulta es `data/raw/*/*/*.parquet` a través de `sql/eda/00_vista.sql` (vista temporal).

## 01_temporal.sql

**Pregunta:** ¿Cuál es el volumen mensual de cada servicio? Comprobar meses disponibles antes de comparar años.

**SQL:**

```sql
-- Meses parciales se muestran tal como están, comparar años completos exige igual ventana.
SELECT tipo, anio_archivo, date_trunc('month', inicio)::DATE AS mes,
       count(*) AS viajes, count(DISTINCT CAST(inicio AS DATE)) AS dias_con_viajes
FROM viajes_b
WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 3, 1;
```

**Resultado e interpretación:** pendientes de ejecución.

## 02_caracteristicas.sql

**Pregunta:** ¿Cómo difieren distancias, duración y pasajeros de yellow y green?

**SQL:**

```sql
SELECT tipo, anio_archivo, count(*) AS viajes,
       round(avg(distancia_millas) FILTER (WHERE distancia_millas > 0 AND distancia_millas < 100), 2) AS distancia_media_filtrada,
       round(median(distancia_millas) FILTER (WHERE distancia_millas > 0 AND distancia_millas < 100), 2) AS distancia_mediana_filtrada,
       round(median(date_diff('minute', inicio, fin)) FILTER
           (WHERE fin >= inicio AND fin <= inicio + INTERVAL '24 hours'), 2) AS duracion_mediana_min,
       round(avg(pasajeros) FILTER (WHERE pasajeros > 0 AND pasajeros <= 8), 2) AS pasajeros_media_filtrada
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado e interpretación:** pendientes de ejecución.

## 03_pago.sql

**Pregunta:** ¿Cómo cambian los porcentajes de códigos de pago y las propinas?

**SQL:**

```sql
-- Código 1 tarjeta y 2 efectivo, verificar con diccionario TLC de cada año.
SELECT tipo, anio_archivo, tipo_pago, count(*) AS viajes,
       round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY tipo, anio_archivo), 2) AS porcentaje,
       round(avg(propina) FILTER (WHERE propina >= 0), 2) AS propina_media_no_negativa
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 1, 3;
```

**Resultado e interpretación:** pendientes de ejecución.

## 04_distribuciones.sql

**Pregunta:** ¿Qué diferencias hay entre medianas y percentiles altos de distancia y total?

**SQL:**

```sql
SELECT tipo, anio_archivo, count(*) AS viajes,
       round(quantile_cont(distancia_millas, 0.5) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p50,
       round(quantile_cont(distancia_millas, 0.95) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p95,
       round(quantile_cont(distancia_millas, 0.99) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p99,
       round(quantile_cont(total, 0.5) FILTER (WHERE total >= 0), 2) AS total_p50,
       round(quantile_cont(total, 0.95) FILTER (WHERE total >= 0), 2) AS total_p95,
       round(quantile_cont(total, 0.99) FILTER (WHERE total >= 0), 2) AS total_p99
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado e interpretación:** pendientes de ejecución.

## 05_atipicos.sql

**Pregunta:** ¿Cuántos viajes presentan valores extremos o duración incoherente?

**SQL:**

```sql
-- Umbrales orientativos de revisión, no reglas de borrado.
SELECT tipo, anio_archivo, count(*) AS viajes,
       count(*) FILTER (WHERE distancia_millas > 100) AS distancia_mayor_100,
       count(*) FILTER (WHERE total > 500) AS total_mayor_500,
       count(*) FILTER (WHERE pasajeros > 8) AS pasajeros_mayor_8,
       count(*) FILTER (WHERE propina > total AND total >= 0) AS propina_mayor_total,
       count(*) FILTER (WHERE fin < inicio OR fin > inicio + INTERVAL '24 hours') AS duracion_invalida
FROM viajes_b GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado e interpretación:** pendientes de ejecución.

## 06_validacion_anios.sql

**Pregunta:** ¿Pueden consultarse juntos los años nuevos?

**SQL:**

```sql
-- Ejecutar tras descargar 2024 y repetir tras incorporar 2025.
SELECT anio_archivo, tipo, count(DISTINCT archivo) AS archivos,
       count(*) AS viajes, min(inicio) AS primera_fecha, max(inicio) AS ultima_fecha
FROM viajes_b
GROUP BY 1, 2 ORDER BY 1, 2;
```

**Resultado e interpretación:** pendientes de ejecución.

## Tres hallazgos por completar

1. Comparación temporal con meses equivalentes, recuentos y denominadores.
2. Comparación de yellow y green en el mismo periodo usando medianas o porcentajes.
3. Describir la cola de una variable junto con una incidencia de calidad, con cifras observadas.

No presentar estas sugerencias como hallazgos hasta completar resultados.
