with enum_data as(
    select 1 as vendor_id, 'Creative Mobile Technologies, LLC' as company_name
    union all
    select 2, 'VeriFone Inc.'
)
select * from enum_data