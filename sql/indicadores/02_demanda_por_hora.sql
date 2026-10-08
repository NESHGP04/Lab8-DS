-- Indicador 2: Demanda por Hora del Día
-- Muestra el volumen de viajes agrupados por hora (0-23) y tipo de taxi.
SELECT 
    CAST(extract('hour' FROM inicio) AS INTEGER) AS hora_dia,
    tipo,
    count(*) AS total_viajes
FROM viajes
WHERE inicio IS NOT NULL
  AND year(inicio) BETWEEN 2024 AND 2026
GROUP BY 1, 2
ORDER BY 1, 2;
