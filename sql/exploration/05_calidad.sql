-- Requiere ejecutar antes sql/eda/00_vista.sql.
SELECT tipo, anio_archivo, count(*) AS viajes,
       count(*) FILTER (WHERE inicio IS NULL OR fin IS NULL) AS fechas_nulas,
       count(*) FILTER (WHERE inicio IS NOT NULL AND year(inicio) <> anio_archivo) AS inicio_fuera_anio,
       count(*) FILTER (WHERE fin < inicio) AS fin_antes_inicio,
       count(*) FILTER (WHERE fin > inicio + INTERVAL '24 hours') AS duracion_mayor_24h,
       count(*) FILTER (WHERE distancia_millas IS NULL) AS distancia_nula,
       count(*) FILTER (WHERE distancia_millas < 0) AS distancia_negativa,
       count(*) FILTER (WHERE distancia_millas = 0) AS distancia_cero,
       count(*) FILTER (WHERE tarifa IS NULL OR total IS NULL) AS importes_nulos,
       count(*) FILTER (WHERE tarifa < 0 OR total < 0) AS importes_negativos,
       count(*) FILTER (WHERE pasajeros IS NULL) AS pasajeros_nulos,
       count(*) FILTER (WHERE pasajeros = 0) AS pasajeros_cero,
       count(*) FILTER (WHERE tipo_pago IS NULL) AS pago_nulo
FROM viajes_b GROUP BY 1, 2 ORDER BY 2, 1;
