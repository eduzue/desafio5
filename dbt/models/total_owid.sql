{{ config(materialized='table',
          enabled=true
          ) 
}}

with 
mortes as (
    select * from {{ref('vw_mortes')}}
),

vacinacao as (
    select * from {{ref('vw_vacinacao')}}
),

casos as (
    select * 
        from {{ref('casos_silver')}}
)

select  casos.data_casos as data_casos,
        vacinacao.data as data_vacinacao,
        mortes.data as data_morte,
        coalesce(casos.data_casos, vacinacao.data, mortes.data) as data,
        casos.local_casos as local_casos,
        mortes.location as local_mortes,
        coalesce(casos.local_casos, mortes.location) as local,
        --
		casos.total_casos - lag(total_casos) over (partition by casos.local_casos order by casos.data_casos) as diaria_casos,
        casos.total_casos,
        casos.total_casos_pm,
        vacinacao.total_vaccinations as total_vacinacao,
        coalesce(vacinacao.daily_vaccinations,0) as diaria_vacinacao,
        vacinacao.daily_vaccinations_per_million as diaria_por_m_vacinacao,
        vacinacao.people_fully_vaccinated as pessoas_total_vacinadas,
        coalesce(mortes.new_deaths,0) as mortes_novas,
        mortes.total_deaths as total_mortes
from casos 
     left outer join
     vacinacao on casos.data_casos = vacinacao.data and casos.local_casos = vacinacao.location
     left outer join
     mortes on casos.data_casos = mortes.data and casos.local_casos = mortes.location
--where   casos.local_casos = 'Brazil'
--        and vacinacao.location = 'Brazil'
--        and mortes.location = 'Brazil'
order by coalesce(casos.data_casos, vacinacao.data, mortes.data)

        


