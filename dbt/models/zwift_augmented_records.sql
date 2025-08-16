{{ config(materialized='table') }}

select
    file_name,
    timestamp,
    DATETIME(timestamp, "America/New_York") as local_timestamp,
    heart_rate,
    power,
    cadence,
    coalesce(speed, enhanced_speed) as speed_ms,
    3.6 * coalesce(speed, enhanced_speed) as speed_kmh,
    
from {{ source('zwift_data', 'zwift_fitfile_records') }}
