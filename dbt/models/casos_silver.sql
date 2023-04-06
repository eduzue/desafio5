{{ config(materialized='table',
          enabled=true
          ) 
}}

with 
casos as (
    select * 
        from {{ref('vw_casos')}}
),

casospm as (
    select * from {{ref('vw_casospm')}}
)

select  casos.data as data_casos,
        casos.localizacao as local_casos,
        casos.casos as total_casos,
        casospm.casos as total_casos_pm
from casos 
     left outer join
     casospm 
        on casos.data = casospm.data 
        and casos.localizacao = casospm.localizacao