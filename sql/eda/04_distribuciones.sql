SELECT tipo, anio_archivo, count(*) AS viajes,
       round(quantile_cont(distancia_millas, 0.5) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p50,
       round(quantile_cont(distancia_millas, 0.95) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p95,
       round(quantile_cont(distancia_millas, 0.99) FILTER (WHERE distancia_millas >= 0), 2) AS distancia_p99,
       round(quantile_cont(total, 0.5) FILTER (WHERE total >= 0), 2) AS total_p50,
       round(quantile_cont(total, 0.95) FILTER (WHERE total >= 0), 2) AS total_p95,
       round(quantile_cont(total, 0.99) FILTER (WHERE total >= 0), 2) AS total_p99
FROM viajes_b WHERE inicio IS NOT NULL AND year(inicio) = anio_archivo
GROUP BY 1, 2 ORDER BY 2, 1;
