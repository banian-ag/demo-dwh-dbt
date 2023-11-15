with date_range as (
    select
            min(least(tpep_pickup_datetime,
            tpep_dropoff_datetime))::date as min_date,
            max(greatest(tpep_pickup_datetime,
            tpep_dropoff_datetime))::date as max_date
    from
            {{ source("raw_data", "nyc_yellow_taxi_trip") }}
),
date_series as (
    select
        generate_series::date as full_date
    from
        generate_series((
        select
            min(min_date)
        from
            date_range),
        (
        select
            max(max_date)
        from
            date_range),
        '1 day'::interval)
)
select 
       full_date,
       to_char(full_date, 'yyyymmdd')::int as full_date_numeric,
       extract(epoch from full_date) as epoch,
       to_char(full_date, 'fmDDth') as day_suffix,
       to_char(full_date, 'TMDay') as day_name,
       extract(isodow from full_date) as day_of_week,
       extract(day from full_date) as day_of_month,
       full_date - date_trunc('quarter', full_date)::date + 1 as day_of_quarter,
       extract(doy from full_date) as day_of_year,
       to_char(full_date, 'W')::int as week_of_month,
       extract(week from full_date) as week_of_year,
       extract(isoyear from full_date) || to_char(full_date, '"-W"IW-') || extract(isodow from full_date) as week_of_year_iso,
       extract(month from full_date) as month_actual,
       to_char(full_date, 'TMMonth') as month_name,
       to_char(full_date, 'Mon') as month_name_abbreviated,
       extract(quarter from full_date) as quarter_actual,
       case
           when extract(quarter from full_date) = 1 then 'First'
           when extract(quarter from full_date) = 2 then 'Second'
           when extract(quarter from full_date) = 3 then 'Third'
           when extract(quarter from full_date) = 4 then 'Fourth'
           end as quarter_name,
       extract(year from full_date) as year_actual,
       full_date + (1 - extract(isodow from full_date))::int as first_day_of_week,
       full_date + (7 - extract(isodow from full_date))::int as last_day_of_week,
       full_date + (1 - extract(day from full_date))::int as first_day_of_month,
       (date_trunc('MONTH', full_date) + INTERVAL '1 MONTH - 1 day')::date as last_day_of_month,
       date_trunc('quarter', full_date)::date as first_day_of_quarter,
       (date_trunc('quarter', full_date) + INTERVAL '3 MONTH - 1 day')::date as last_day_of_quarter,
       to_date(extract(year from full_date) || '-01-01', 'YYYY-MM-DD') as first_day_of_year,
       to_date(extract(year from full_date) || '-12-31', 'YYYY-MM-DD') as last_day_of_year,
       to_char(full_date, 'mmyyyy') as mmyyyy,
       to_char(full_date, 'mmddyyyy') as mmddyyyy,
       case
           when extract(isodow from full_date) in (6, 7) then true
           else false
           end as is_weekend,
       case
           when extract(isodow from full_date) in (6,7) then false
           else true
           end as is_weekday
from date_series