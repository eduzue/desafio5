{{ config(materialized='table',
          enabled=true
          ) 
}}

with 
total as (
    select * from {{ref('total_owid')}}
)

select  total.data,
        total.local,
        --
	coalesce(total.diaria_casos,0) as diaria_casos,
        total.diaria_vacinacao,
        total.mortes_novas
from total
order by local, data