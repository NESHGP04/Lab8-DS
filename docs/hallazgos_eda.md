# EDA: preguntas, consultas y resultados

Fuente de todas las consultas: `data/raw/*/*/*.parquet`; ejecutar antes `sql/eda/00_vista.sql` (vista temporal, no materialización).

## 01_temporal.sql

**Pregunta y justificación:** ¿Qué volumen mensual corresponde a cada tipo y año? Los archivos contienen las variables necesarias para responderla.

**SQL:**

```sql
-- Meses parciales se muestran tal como están, comparar años completos exige igual ventana.
SELECT tipo, anio_archivo, date_trunc('month', inicio)::DATE AS mes,
       count(*) AS viajes, count(DISTINCT CAST(inicio AS DATE)) AS dias_con_viajes
FROM viajes_b
WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 3, 1;
```

**Resultado:**

| tipo | anio_archivo | mes | viajes | dias_con_viajes |
| --- | --- | --- | --- | --- |
| green | 2024 | 2024-01-01 | 56555 | 31 |
| yellow | 2024 | 2024-01-01 | 2964617 | 31 |
| green | 2024 | 2024-02-01 | 53578 | 29 |
| yellow | 2024 | 2024-02-01 | 3007533 | 29 |
| green | 2024 | 2024-03-01 | 57451 | 31 |
| yellow | 2024 | 2024-03-01 | 3582611 | 31 |
| green | 2024 | 2024-04-01 | 56473 | 30 |
| yellow | 2024 | 2024-04-01 | 3514295 | 30 |
| green | 2024 | 2024-05-01 | 61007 | 31 |
| yellow | 2024 | 2024-05-01 | 3723843 | 31 |
| green | 2024 | 2024-06-01 | 54738 | 30 |
| yellow | 2024 | 2024-06-01 | 3539170 | 30 |
| green | 2024 | 2024-07-01 | 51820 | 31 |
| yellow | 2024 | 2024-07-01 | 3076876 | 31 |
| green | 2024 | 2024-08-01 | 51806 | 31 |
| yellow | 2024 | 2024-08-01 | 2979192 | 31 |
| green | 2024 | 2024-09-01 | 54422 | 30 |
| yellow | 2024 | 2024-09-01 | 3633025 | 30 |
| green | 2024 | 2024-10-01 | 56153 | 31 |
| yellow | 2024 | 2024-10-01 | 3833780 | 31 |
| green | 2024 | 2024-11-01 | 52214 | 30 |
| yellow | 2024 | 2024-11-01 | 3646372 | 30 |
| green | 2024 | 2024-12-01 | 53981 | 31 |
| yellow | 2024 | 2024-12-01 | 3668350 | 31 |
| green | 2025 | 2025-01-01 | 48288 | 31 |
| yellow | 2025 | 2025-01-01 | 3475234 | 31 |
| green | 2025 | 2025-02-01 | 46645 | 28 |
| yellow | 2025 | 2025-02-01 | 3577542 | 28 |
| green | 2025 | 2025-03-01 | 51550 | 31 |
| yellow | 2025 | 2025-03-01 | 4145229 | 31 |
| green | 2025 | 2025-04-01 | 52134 | 30 |
| yellow | 2025 | 2025-04-01 | 3970568 | 30 |
| green | 2025 | 2025-05-01 | 55405 | 31 |
| yellow | 2025 | 2025-05-01 | 4591844 | 31 |
| green | 2025 | 2025-06-01 | 49385 | 30 |
| yellow | 2025 | 2025-06-01 | 4322949 | 30 |
| green | 2025 | 2025-07-01 | 48202 | 31 |
| yellow | 2025 | 2025-07-01 | 3898971 | 31 |
| green | 2025 | 2025-08-01 | 46305 | 31 |
| yellow | 2025 | 2025-08-01 | 3574080 | 31 |
| green | 2025 | 2025-09-01 | 48885 | 30 |
| yellow | 2025 | 2025-09-01 | 4251019 | 30 |
| green | 2025 | 2025-10-01 | 49417 | 31 |
| yellow | 2025 | 2025-10-01 | 4428708 | 31 |
| green | 2025 | 2025-11-01 | 46915 | 30 |
| yellow | 2025 | 2025-11-01 | 4181432 | 30 |
| green | 2025 | 2025-12-01 | 48223 | 31 |
| yellow | 2025 | 2025-12-01 | 4304997 | 31 |
| green | 2026 | 2026-01-01 | 40258 | 31 |
| yellow | 2026 | 2026-01-01 | 3724894 | 31 |
| green | 2026 | 2026-02-01 | 37388 | 28 |
| yellow | 2026 | 2026-02-01 | 3399866 | 28 |
| green | 2026 | 2026-03-01 | 44203 | 31 |
| yellow | 2026 | 2026-03-01 | 3952443 | 31 |
| green | 2026 | 2026-04-01 | 44243 | 30 |
| yellow | 2026 | 2026-04-01 | 3831256 | 30 |
| green | 2026 | 2026-05-01 | 44925 | 31 |
| yellow | 2026 | 2026-05-01 | 4090824 | 31 |
| green | 2026 | 2026-06-01 | 44156 | 30 |
| yellow | 2026 | 2026-06-01 | 3837239 | 30 |
| green | 2026 | 2026-07-01 | 41249 | 31 |
| yellow | 2026 | 2026-07-01 | 3530077 | 31 |
| green | 2026 | 2026-08-01 | 40678 | 31 |
| yellow | 2026 | 2026-08-01 | 3336739 | 31 |

64 filas de salida; se muestran hasta 80.

**Interpretación:** Comparar meses equivalentes y revisar días de cobertura. Explicar las cifras anteriores antes de la entrega.

## 02_caracteristicas.sql

**Pregunta y justificación:** ¿Qué distancia, duración y ocupación tiene el viaje típico? Los archivos contienen las variables necesarias para responderla.

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

**Resultado:**

| tipo | anio_archivo | viajes | distancia_media_filtrada | distancia_mediana_filtrada | duracion_mediana_min | pasajeros_media_filtrada |
| --- | --- | --- | --- | --- | --- | --- |
| green | 2024 | 660198 | 2.94 | 1.97 | 12.0 | 1.33 |
| yellow | 2024 | 41169664 | 3.43 | 1.8 | 13.0 | 1.35 |
| green | 2025 | 591354 | 3.19 | 2.06 | 13.0 | 1.31 |
| yellow | 2025 | 48722573 | 3.5 | 1.9 | 13.0 | 1.3 |
| green | 2026 | 337100 | 3.36 | 2.14 | 13.0 | 1.32 |
| yellow | 2026 | 29703338 | 3.51 | 1.92 | 14.0 | 1.25 |

6 filas de salida; se muestran hasta 80.

**Interpretación:** Comparar mediana y media filtrada dentro del mismo periodo. Explicar las cifras anteriores antes de la entrega.

## 03_pago.sql

**Pregunta y justificación:** ¿Qué códigos de pago predominan? Los archivos contienen las variables necesarias para responderla.

**SQL:**

```sql
-- Código 1 tarjeta y 2 efectivo, verificar con diccionario TLC de cada año.
SELECT tipo, anio_archivo, tipo_pago, count(*) AS viajes,
       round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY tipo, anio_archivo), 2) AS porcentaje,
       round(avg(propina) FILTER (WHERE propina >= 0), 2) AS propina_media_no_negativa
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 1, 3;
```

**Resultado:**

| tipo | anio_archivo | tipo_pago | viajes | porcentaje | propina_media_no_negativa |
| --- | --- | --- | --- | --- | --- |
| green | 2024 | 1 | 454677 | 68.87 | 3.55 |
| green | 2024 | 2 | 175005 | 26.51 | 0.0 |
| green | 2024 | 3 | 4598 | 0.7 | 0.03 |
| green | 2024 | 4 | 1561 | 0.24 | 0.02 |
| green | 2024 | 5 | 29 | 0.0 | 0.0 |
| green | 2024 | NULL | 24328 | 3.68 | 3.58 |
| yellow | 2024 | 0 | 4091232 | 9.94 | 0.76 |
| yellow | 2024 | 1 | 30452126 | 73.97 | 4.37 |
| yellow | 2024 | 2 | 5540067 | 13.46 | 0.0 |
| yellow | 2024 | 3 | 291741 | 0.71 | 0.03 |
| yellow | 2024 | 4 | 794494 | 1.93 | 0.06 |
| yellow | 2024 | 5 | 4 | 0.0 | 0.0 |
| green | 2025 | 1 | 406600 | 68.76 | 3.69 |
| green | 2025 | 2 | 129823 | 21.95 | 0.0 |
| green | 2025 | 3 | 3784 | 0.64 | 0.05 |
| green | 2025 | 4 | 1244 | 0.21 | 0.01 |
| green | 2025 | 5 | 23 | 0.0 | 0.0 |
| green | 2025 | NULL | 49880 | 8.43 | 1.51 |
| yellow | 2025 | 0 | 11611894 | 23.83 | 0.33 |
| yellow | 2025 | 1 | 31053982 | 63.74 | 4.34 |
| yellow | 2025 | 2 | 4654334 | 9.55 | 0.0 |
| yellow | 2025 | 3 | 308147 | 0.63 | 0.02 |
| yellow | 2025 | 4 | 1094213 | 2.25 | 0.02 |
| yellow | 2025 | 5 | 3 | 0.0 | 0.0 |
| green | 2026 | 1 | 219974 | 65.25 | 3.84 |
| green | 2026 | 2 | 65913 | 19.55 | 0.0 |
| green | 2026 | 3 | 1688 | 0.5 | 0.01 |
| green | 2026 | 4 | 750 | 0.22 | 0.0 |
| green | 2026 | NULL | 48775 | 14.47 | 0.79 |
| yellow | 2026 | 0 | 7716688 | 25.98 | 0.4 |
| yellow | 2026 | 1 | 18940999 | 63.77 | 4.28 |
| yellow | 2026 | 2 | 2708025 | 9.12 | 0.0 |
| yellow | 2026 | 3 | 98136 | 0.33 | 0.0 |
| yellow | 2026 | 4 | 239488 | 0.81 | 0.0 |
| yellow | 2026 | 5 | 2 | 0.0 | 0.0 |

35 filas de salida; se muestran hasta 80.

**Interpretación:** Comparar porcentajes; consultar el diccionario TLC antes de etiquetar códigos. Explicar las cifras anteriores antes de la entrega.

## 04_distribuciones.sql

**Pregunta y justificación:** ¿Qué tan largas son las colas de montos y distancias? Los archivos contienen las variables necesarias para responderla.

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

**Resultado:**

| tipo | anio_archivo | viajes | distancia_p50 | distancia_p95 | distancia_p99 | total_p50 | total_p95 | total_p99 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| green | 2024 | 660198 | 1.87 | 8.49 | 16.4 | 19.32 | 56.25 | 95.8 |
| yellow | 2024 | 41169664 | 1.76 | 14.3 | 20.05 | 21.12 | 82.69 | 104.88 |
| green | 2025 | 591354 | 1.98 | 9.79 | 17.6 | 20.04 | 58.5 | 99.48 |
| yellow | 2025 | 48722573 | 1.85 | 12.75 | 19.55 | 21.54 | 77.94 | 104.88 |
| green | 2026 | 337100 | 2.07 | 10.52 | 17.76 | 20.5 | 57.72 | 97.2 |
| yellow | 2026 | 29703338 | 1.86 | 12.3 | 19.5 | 23.69 | 77.75 | 105.75 |

6 filas de salida; se muestran hasta 80.

**Interpretación:** Comparar p50, p95 y p99 sin equiparar extremo a error. Explicar las cifras anteriores antes de la entrega.

## 05_atipicos.sql

**Pregunta y justificación:** ¿Cuántos valores exceden umbrales de revisión? Los archivos contienen las variables necesarias para responderla.

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

**Resultado:**

| tipo | anio_archivo | viajes | distancia_mayor_100 | total_mayor_500 | pasajeros_mayor_8 | propina_mayor_total | duracion_invalida |
| --- | --- | --- | --- | --- | --- | --- | --- |
| green | 2024 | 660218 | 235 | 36 | 48 | 4 | 2 |
| yellow | 2024 | 41169720 | 1613 | 831 | 36 | 80 | 1805 |
| green | 2025 | 591375 | 209 | 27 | 58 | 0 | 1346 |
| yellow | 2025 | 48722602 | 2870 | 1210 | 34 | 58 | 2587 |
| green | 2026 | 337114 | 72 | 21 | 31 | 1 | 9 |
| yellow | 2026 | 29703355 | 1223 | 791 | 6 | 140 | 273 |

6 filas de salida; se muestran hasta 80.

**Interpretación:** Reportar recuentos y porcentajes; no eliminar correcciones de pago a ciegas. Explicar las cifras anteriores antes de la entrega.

## 06_validacion_anios.sql

**Pregunta y justificación:** ¿Están presentes ambos tipos en 2024, 2025 y 2026? Los archivos contienen las variables necesarias para responderla.

**SQL:**

```sql
-- Ejecutar tras descargar 2024 y repetir tras incorporar 2025.
SELECT anio_archivo, tipo, count(DISTINCT archivo) AS archivos,
       count(*) AS viajes, min(inicio) AS primera_fecha, max(inicio) AS ultima_fecha
FROM viajes_b
GROUP BY 1, 2 ORDER BY 1, 2;
```

**Resultado:**

| anio_archivo | tipo | archivos | viajes | primera_fecha | ultima_fecha |
| --- | --- | --- | --- | --- | --- |
| 2024 | green | 12 | 660218 | 2008-12-31 00:00:00 | 2025-01-01 22:21:15 |
| 2024 | yellow | 12 | 41169720 | 2002-12-31 16:46:07 | 2026-06-26 23:53:12 |
| 2025 | green | 12 | 591375 | 2008-12-31 15:13:04 | 2026-01-01 21:09:39 |
| 2025 | yellow | 12 | 48722602 | 2007-12-05 18:45:00 | 2025-12-31 23:59:59 |
| 2026 | green | 8 | 337114 | 2008-12-31 17:35:31 | 2026-08-31 23:58:28 |
| 2026 | yellow | 8 | 29703355 | 2001-01-01 09:23:58 | 2026-08-31 23:59:59 |

6 filas de salida; se muestran hasta 80.

**Interpretación:** Distinguir ausencia de archivos de ausencia de viajes. Explicar las cifras anteriores antes de la entrega.

## Tres hallazgos que completar con evidencia

1. Temporal: señalar tipo, meses comparables, conteos y cambio porcentual; corregir cobertura parcial.
2. Yellow frente a green: para el mismo periodo contrastar medianas de distancia/duración o porcentajes de pago.
3. Distribución y calidad: señalar p50/p99 y una incidencia con numerador y denominador.

Estas son preguntas para redactar hallazgos, no resultados observados. Completar las tres frases después de examinar las tablas.

