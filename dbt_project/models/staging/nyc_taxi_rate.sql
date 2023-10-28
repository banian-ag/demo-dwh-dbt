with enum_data as (
    select 1 as rate_id, 'Standard rate' as rate_name union all
    select 2, 'JFK' union all
    select 3, 'Newark' union all
    select 4, 'Nassau or Westchester' union all
    select 5, 'Negotiated fare' union all
    select 6, 'Group ride'
)
select * from enum_data