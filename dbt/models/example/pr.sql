{{ config(materialized='table') }}

select product_key, product_name
from {{ source('TEST', 'dim_products') }}