with enum_data as (
    select 1 as payment_type_id, 'Credit card' as payment_type
    union all
    select 2, 'Cash'
    union all
    select 3, 'No charge'
    union all
    select 4, 'Dispute'
    union all
    select 5, 'Unknown'
    union all
    select 6, 'Voided trip'
)
select * from enum_data