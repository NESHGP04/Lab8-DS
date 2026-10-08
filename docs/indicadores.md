# Ejercicio 7: Construcción de Indicadores y Tablero

## 1. Preguntas de Análisis (7.1)

1. ¿Cómo varía el volumen de viajes a lo largo de los meses para identificar estacionalidad?
2. ¿Cuáles son las horas del día con mayor y menor demanda de taxis?
3. ¿Qué porcentaje de los viajes se origina en cada Borough (distrito) y cómo difiere entre taxis amarillos y verdes?
4. ¿Cuál es la preferencia de método de pago de los usuarios (Tarjeta vs Efectivo)?
5. ¿De qué manera el método de pago afecta el porcentaje de propina que dejan los pasajeros?
6. ¿Cuál es la tarifa promedio por milla recorrida y cómo ha cambiado en el tiempo?
7. ¿Existen diferencias significativas en la duración promedio de un viaje en días de semana vs. fines de semana?
8. ¿Qué porcentaje de los ingresos totales de los taxis provienen de viajes hacia los aeropuertos (JFK, LaGuardia, Newark)?
9. ¿Cuál es la distribución típica de pasajeros por viaje (viajes en solitario vs. grupos)?
10. ¿Cómo es el rendimiento (ingreso total por viaje) de los taxis amarillos en comparación con los verdes?

---

## 2. Los 6 Indicadores Seleccionados, Consultas y Justificación

### Indicador 1: Tendencia Mensual de Viajes

- **Pregunta:** ¿Cómo varía el volumen de viajes a lo largo de los meses?
- **Justificación:** Esencial para detectar estacionalidad (ej. bajas en invierno, alzas en verano) y el impacto histórico de la operación entre 2024 y 2026.
- **SQL:** [`sql/indicadores/01_tendencia_mensual.sql`](../sql/indicadores/01_tendencia_mensual.sql)

### Indicador 2: Demanda por Hora del Día

- **Pregunta:** ¿Cuáles son las horas con mayor demanda?
- **Justificación:** Determina las horas punta (Rush Hour), vital para la gestión de flota y asignación de turnos.
- **SQL:** [`sql/indicadores/02_demanda_por_hora.sql`](../sql/indicadores/02_demanda_por_hora.sql)

### Indicador 3: Distribución de Recogidas por Distrito

- **Pregunta:** ¿De dónde salen más viajes para cada tipo de taxi?
- **Justificación:** Permite visualizar cómo los taxis verdes dominan zonas periféricas (Brooklyn, Queens) mientras los amarillos se concentran en Manhattan.
- **SQL:** [`sql/indicadores/03_distritos_origen.sql`](../sql/indicadores/03_distritos_origen.sql)

### Indicador 4: Propinas según Método de Pago

- **Pregunta:** ¿Cómo afecta el pago en efectivo o tarjeta a las propinas?
- **Justificación:** Las propinas en tarjeta se registran mejor y suelen tener porcentajes sugeridos, lo cual impacta el ingreso del conductor.
- **SQL:** [`sql/indicadores/04_propinas_pago.sql`](../sql/indicadores/04_propinas_pago.sql)

### Indicador 5: Tarifa Promedio por Milla

- **Pregunta:** ¿Cuál es la rentabilidad de cada viaje por unidad de distancia?
- **Justificación:** La tarifa por milla indica si la flota está maximizando sus ganancias considerando el tiempo y distancia recorridos.
- **SQL:** [`sql/indicadores/05_tarifa_milla.sql`](../sql/indicadores/05_tarifa_milla.sql)

### Indicador 6: Impacto de los Viajes a Aeropuertos

- **Pregunta:** ¿Qué tan importantes son los viajes a los aeropuertos para el negocio?
- **Justificación:** Los aeropuertos son rutas de alto valor (High-Ticket). Conocer este porcentaje indica la salud de este nicho específico de negocio.
- **SQL:** [`sql/indicadores/06_aeropuertos.sql`](../sql/indicadores/06_aeropuertos.sql)

---

## 3. Interpretación de Resultados y Hallazgos

A partir de los resultados obtenidos tras visualizar estas consultas (ver gráficas en `notebooks/04_indicadores.ipynb` y Metabase), se encuentran los siguientes hallazgos:

1. El Indicador 3 muestra que más del 85% de los viajes de taxis amarillos se originan en Manhattan, confirmando que este servicio es predominantemente central, mientras que los taxis verdes tienen una fuerte presencia en Brooklyn, Queens y el Norte de Manhattan.
2. El Indicador 6 revela un patrón fascinante. Aunque los viajes hacia aeropuertos representan una fracción pequeña del volumen total de viajes (usualmente < 5%), generan un porcentaje del ingreso total (Total Amount) casi 3 veces mayor (alrededor del 15%). Esto confirma que captar viajes de aeropuerto es extremadamente rentable.
3. El Indicador 4 demuestra que los viajes pagados con tarjeta de crédito registran consistentemente más propinas. En muchos registros de pago en efectivo, la propina registrada en sistema es $0, probablemente porque la propina en efectivo no se declara o se maneja fuera del medidor.
4. El mapa de calor de horas (Indicador 2) refleja una baja demanda a las 4:00 AM, subiendo a un pico por la tarde (17:00 - 19:00 hrs) que coincide con el final de la jornada laboral en NY. Curiosamente, la demanda nocturna en fines de semana no compensa el altísimo volumen de oficinistas entre semana.
