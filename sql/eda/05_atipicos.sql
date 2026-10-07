-- Umbrales orientativos de revisión, no reglas de borrado.
SELECT tipo, anio_archivo, count(*) AS viajes,
       count(*) FILTER (WHERE distancia_millas > 100) AS distancia_mayor_100,
       count(*) FILTER (WHERE total > 500) AS total_mayor_500,
       count(*) FILTER (WHERE pasajeros > 8) AS pasajeros_mayor_8,
       count(*) FILTER (WHERE propina > total AND total >= 0) AS propina_mayor_total,
       count(*) FILTER (WHERE fin < inicio OR fin > inicio + INTERVAL '24 hours') AS duracion_invalida
FROM viajes_b GROUP BY 1, 2 ORDER BY 2, 1;
