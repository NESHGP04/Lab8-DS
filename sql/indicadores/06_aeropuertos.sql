-- Indicador 6: Impacto Económico de Viajes a Aeropuertos
-- Porcentaje de ingresos y volumen generados por viajes con destino a aeropuertos.
SELECT 
    date_trunc('month', v.inicio)::DATE AS mes,
    v.tipo,
    SUM(CASE WHEN z.Zone ILIKE '%Airport%' THEN 1 ELSE 0 END) AS viajes_aeropuerto,
    COUNT(*) AS viajes_totales,
    SUM(CASE WHEN z.Zone ILIKE '%Airport%' THEN v.total ELSE 0 END) AS ingresos_aeropuerto,
    SUM(v.total) AS ingresos_totales,
    (SUM(CASE WHEN z.Zone ILIKE '%Airport%' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0)) AS pct_viajes_aeropuerto,
    (SUM(CASE WHEN z.Zone ILIKE '%Airport%' THEN v.total ELSE 0 END) * 100.0 / NULLIF(SUM(v.total), 0)) AS pct_ingresos_aeropuerto
FROM viajes v
JOIN zonas z ON v.zona_destino = z.LocationID
WHERE v.inicio IS NOT NULL 
  AND year(v.inicio) BETWEEN 2024 AND 2026
  AND v.total > 0
GROUP BY 1, 2
ORDER BY 1, 2;
