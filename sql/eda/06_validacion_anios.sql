-- Ejecutar tras descargar 2024 y repetir tras incorporar 2025.
SELECT anio_archivo, tipo, count(DISTINCT archivo) AS archivos,
       count(*) AS viajes, min(inicio) AS primera_fecha, max(inicio) AS ultima_fecha
FROM viajes_b
GROUP BY 1, 2 ORDER BY 1, 2;
