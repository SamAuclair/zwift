{{ config(materialized='table') }}

select
    file_name,
    DATETIME(timestamp, "America/New_York") as local_timestamp,
    DATE(DATETIME(timestamp, "America/New_York")) as date,
    TIME(DATETIME(timestamp, "America/New_York")) as time,
    heart_rate,
    power,
    cadence,
    coalesce(speed, enhanced_speed) as speed_ms,
    3.6 * coalesce(speed, enhanced_speed) as speed_kmh,
    
from {{ source('zwift_data', 'fitfile_data') }}
