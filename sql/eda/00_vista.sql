-- Ejecutar al inicio de cada sesión. Consulta directamente Parquet, no persiste datos.
CREATE OR REPLACE TEMP VIEW viajes_b AS
SELECT
    regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
    TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
    filename AS archivo,
    COALESCE(TRY_CAST(tpep_pickup_datetime AS TIMESTAMP), TRY_CAST(lpep_pickup_datetime AS TIMESTAMP)) AS inicio,
    COALESCE(TRY_CAST(tpep_dropoff_datetime AS TIMESTAMP), TRY_CAST(lpep_dropoff_datetime AS TIMESTAMP)) AS fin,
    TRY_CAST(passenger_count AS DOUBLE) AS pasajeros,
    TRY_CAST(trip_distance AS DOUBLE) AS distancia_millas,
    TRY_CAST(fare_amount AS DOUBLE) AS tarifa,
    TRY_CAST(total_amount AS DOUBLE) AS total,
    TRY_CAST(tip_amount AS DOUBLE) AS propina,
    TRY_CAST(payment_type AS INTEGER) AS tipo_pago
FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false);
