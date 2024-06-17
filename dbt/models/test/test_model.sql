{{ config(materialized='table') }}

SELECT                                                                                                                                                               
    cust_sales AS attribute_code,                                                                                                                                    
    cust_sales_description AS attribute_desc,                                                                                                                        
    beam_party_key AS party_key
FROM {{ source('thebar_gl_raw_SRC', 'edw_customer') }}