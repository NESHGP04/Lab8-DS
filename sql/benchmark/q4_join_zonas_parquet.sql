-- Q4: JOIN con zonas — top 10 zonas de recogida por volumen de viajes.
-- Version PARQUET
SELECT z.Zone AS zona, z.Borough AS borough, count(*) AS viajes
FROM read_parquet('{glob}', union_by_name = true, filename = true, hive_partitioning = false) t
JOIN read_csv_auto('data/raw/zonas/taxi_zone_lookup.csv') z
  ON TRY_CAST(t.PULocationID AS INTEGER) = z.LocationID
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;
