-- Indicador 1: Tendencia Mensual de Viajes (Volumen)
-- Muestra el total de viajes por mes y tipo de taxi.
SELECT 
    date_trunc('month', inicio)::DATE AS mes,
    tipo,
    count(*) AS total_viajes
FROM viajes
WHERE inicio IS NOT NULL
  AND year(inicio) BETWEEN 2024 AND 2026
GROUP BY 1, 2
ORDER BY 1, 2;
