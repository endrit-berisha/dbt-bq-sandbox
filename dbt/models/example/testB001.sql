{{ config(materialized='table') }}

with fact as (
    select *
    from {{ source('TEST', 'fact_depletions') }}
),

products as (
    select *
    from {{ source('TEST', 'dim_products') }}
)

select 
    f.product_key,
    f.actual_gross_sales,
    p.product_name,
    f.actual_volume_9l * p.cost_price as total_value
from fact f
join products p
on f.product_key = p.product_key
where f.product_key = 'B001'