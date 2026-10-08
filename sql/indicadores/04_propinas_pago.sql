-- Indicador 4: Propinas según Método de Pago
-- Relación entre el método de pago (Tarjeta vs Efectivo) y el porcentaje de propina.
SELECT 
    tipo_pago,
    CASE 
        WHEN tipo_pago = 1 THEN 'Credit card'
        WHEN tipo_pago = 2 THEN 'Cash'
        ELSE 'Other'
    END AS descripcion_pago,
    count(*) AS total_viajes,
    avg(propina) AS propina_promedio,
    avg(propina / NULLIF(total, 0)) * 100 AS porcentaje_propina_promedio
FROM viajes
WHERE tipo_pago IN (1, 2) AND total > 0 AND propina >= 0
GROUP BY 1, 2
ORDER BY 1;
