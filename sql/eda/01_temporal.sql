-- Meses parciales se muestran tal como están, comparar años completos exige igual ventana.
SELECT tipo, anio_archivo, date_trunc('month', inicio)::DATE AS mes,
       count(*) AS viajes, count(DISTINCT CAST(inicio AS DATE)) AS dias_con_viajes
FROM viajes_b
WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2, 3 ORDER BY 2, 3, 1;
