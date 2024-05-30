{{ config(materialized='table') }}


select *
from {{ source('TEST', 'dim_products') }}
where product_key = "B001"
