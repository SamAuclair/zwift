{{ config(materialized='table') }}

select
    date,
    sum(case when percent_of_max_hr < 0.6 then 1 else 0 end) as time_zone_1,
    sum(case when percent_of_max_hr >= 0.6 and percent_of_max_hr < 0.7 then 1 else 0 end) as time_zone_2,
    sum(case when percent_of_max_hr >= 0.7 and percent_of_max_hr < 0.8 then 1 else 0 end) as time_zone_3,
    sum(case when percent_of_max_hr >= 0.8 and percent_of_max_hr < 0.9 then 1 else 0 end) as time_zone_4,
    sum(case when percent_of_max_hr >= 0.9 then 1 else 0 end) as time_zone_5,
    sum(case when percent_of_max_hr < 0.6 then 1 else 0 end)/count(date) as percentage_time_zone_1,
    sum(case when percent_of_max_hr >= 0.6 and percent_of_max_hr < 0.7 then 1 else 0 end)/count(date) as percentage_time_zone_2,
    sum(case when percent_of_max_hr >= 0.7 and percent_of_max_hr < 0.8 then 1 else 0 end)/count(date) as percentage_time_zone_3,
    sum(case when percent_of_max_hr >= 0.8 and percent_of_max_hr < 0.9 then 1 else 0 end)/count(date) as percentage_time_zone_4,
    sum(case when percent_of_max_hr >= 0.9 then 1 else 0 end)/count(date) as percentage_time_zone_5
from (
    select
        date,
        heart_rate / (220 - DATE_DIFF(DATE(local_timestamp), DATE('1994-05-12'), YEAR)) as percent_of_max_hr
    from {{ ref('augmented_data') }}
    where heart_rate is not null
) as fitfile_data
group by date
order by date desc