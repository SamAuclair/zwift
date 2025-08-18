{{ config(materialized='table') }}

select
    file_name,
    min(local_timestamp) as start_time,
    max(local_timestamp) as end_time,
    DATETIME_DIFF(max(local_timestamp), min(local_timestamp), SECOND) as duration,
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
group by file_name
having DATETIME_DIFF(max(local_timestamp), min(local_timestamp), SECOND) >= 600
order by min(local_timestamp) desc