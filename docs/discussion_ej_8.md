# Ejercicio 8: Discusión — Impacto de Nuevos Datos (2025)

## 8.5 y 8.6 Análisis Evolutivo (2024 - 2026) y Patrones Encontrados

Al actualizar nuestro tablero en Metabase con el nuevo flujo de datos (121 millones de filas), el vacío de información del 2025 se llenó de forma continua, revelando los siguientes tres patrones clave en la evolución del servicio:

1. **Estabilidad y Resiliencia del Volumen (Indicador 1):**
   Al observar la tendencia mensual continua desde 2024 hasta 2026, notamos que el volumen de los taxis amarillos se mantiene fuertemente en una franja de entre 3.0 y 4.5 millones de viajes mensuales. Se observa un patrón estacional clásico: caídas predecibles en los meses más fríos de invierno (Enero/Febrero) y un repunte fuerte hacia la primavera y el verano. La incursión del 2025 no muestra una disrupción, sino una sólida consolidación post-pandemia.

2. **Dinamismo en la Tarifa por Milla (Indicador 5):**
   Antes de ingresar los datos de 2025, el gráfico de tarifa por milla mostraba una falsa línea de interpolación. Con los datos reales, se hace visible que la rentabilidad por milla tiene picos y valles muy marcados, que probablemente coincidan con semanas de alta demanda, incrementos de tráfico o cambios en la regulación de tarifas de la ciudad. A lo largo de los 3 años, la métrica logra estabilizarse alrededor de los $4.00 - $6.00 por milla.

3. **Mina de Oro Consistente en Aeropuertos (Indicador 6):**
   A lo largo de los tres años (2024, 2025, y 2026), el porcentaje de ingresos provenientes de viajes al aeropuerto se mantiene consistentemente por encima del volumen de viajes físicos que representan. Este no fue un fenómeno aislado del 2024, sino una regla de negocio consolidada. Representan menos del 5% del volumen total, pero entre un 8% y 15% del ingreso en la ventana de tres años.

## 8.7 Documentación de Consultas

Las consultas SQL utilizadas para generar los seis indicadores sobre la base de datos ampliada se encuentran documentadas en la ruta: sql/indicadores/ Los resultados fueron visualizados utilizando Metabase, conectándose de forma nativa a taxis.duckdb.
