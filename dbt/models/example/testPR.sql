{{ config(materialized='table') }}

select *
from {{ source('TEST', 'dim_distributors') }}