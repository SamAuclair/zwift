{{ config(materialized='table') }}

select
    file_name,
    sum(case when percent_of_max_hr < 0.6 then 1 else 0 end) as time_zone_1,
    sum(case when percent_of_max_hr >= 0.6 and percent_of_max_hr < 0.7 then 1 else 0 end) as time_zone_2,
    sum(case when percent_of_max_hr >= 0.7 and percent_of_max_hr < 0.8 then 1 else 0 end) as time_zone_3,
    sum(case when percent_of_max_hr >= 0.8 and percent_of_max_hr < 0.9 then 1 else 0 end) as time_zone_4,
    sum(case when percent_of_max_hr >= 0.9 then 1 else 0 end) as time_zone_5
from (
    select
        file_name,
        timestamp,
        heart_rate / (220 - DATE_DIFF(DATE(timestamp), DATE('1994-05-12'), YEAR)) as percent_of_max_hr
    from {{ source('zwift_data', 'fitfile_data') }}
    where heart_rate is not null
) as fitfile_data
group by file_name
order by file_name desc