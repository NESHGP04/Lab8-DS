SELECT tipo, anio_archivo, count(*) AS viajes,
       round(avg(distancia_millas) FILTER (WHERE distancia_millas > 0 AND distancia_millas < 100), 2) AS distancia_media_filtrada,
       round(median(distancia_millas) FILTER (WHERE distancia_millas > 0 AND distancia_millas < 100), 2) AS distancia_mediana_filtrada,
       round(median(date_diff('minute', inicio, fin)) FILTER
           (WHERE fin >= inicio AND fin <= inicio + INTERVAL '24 hours'), 2) AS duracion_mediana_min,
       round(avg(pasajeros) FILTER (WHERE pasajeros > 0 AND pasajeros <= 8), 2) AS pasajeros_media_filtrada
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2 ORDER BY 2, 1;
