-- Código 1 tarjeta y 2 efectivo, verificar con diccionario TLC de cada año.
SELECT tipo, anio_archivo, tipo_pago, count(*) AS viajes,
       round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY tipo, anio_archivo), 2) AS porcentaje,
       round(avg(propina) FILTER (WHERE propina >= 0), 2) AS propina_media_no_negativa
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 1, 3;
