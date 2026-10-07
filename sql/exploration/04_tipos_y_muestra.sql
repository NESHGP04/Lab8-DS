-- Ejecutar las dos sentencias por separado en el notebook.
DESCRIBE SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false);
SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false) LIMIT 5;
