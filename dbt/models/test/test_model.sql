{{ config(materialized='table') }}

SELECT                                                                                                                                                               
    CONCAT(
      COALESCE(cust_sales, 'NAN'),
      '~',
      COALESCE(distr_chan, 'NAN'),
      '~',
      COALESCE(division, 'NAN'),
      '~',
      COALESCE(salesorg, 'NAN')
    ) AS beam_party_key
FROM {{ source('thebar_gl_raw_SRC', 'edw_customer') }}