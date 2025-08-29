{{ config(materialized='table') }}

select
    date,
    min(time) as start_time,
    max(time) as end_time,
    TIME_DIFF(max(time), min(time), SECOND) as duration,
    round(sum(speed_ms)/ 1000, 1) as distance_km,
    round(avg(speed_kmh), 1) as avg_speed_kmh,
    round(avg(power), 0) as avg_power,
    round(avg(heart_rate), 0) as avg_heart_rate,
    round(avg(cadence), 0) as avg_cadence,
    round(max(heart_rate), 0) as max_heart_rate,
    round(max(power), 0) as max_power,
    round(max(cadence), 0) as max_cadence,
    round(max(speed_kmh), 1) as max_speed_kmh
    
from {{ ref('augmented_data') }}
group by date
order by date desc