{{ config(materialized='view',
          enabled=true
          ) 
}}
select  date||'_'||replace(location, ' ','_') as chave,
        to_date("date", 'yyyy-mm-dd') as data,                           	
        location,                   
        new_cases::bigint AS new_cases,      
        new_deaths::bigint as new_deaths,
        total_cases::bigint  as total_cases  ,
        total_deaths::bigint as total_deaths  ,
        weekly_cases::bigint  as weekly_cases ,
        weekly_deaths::bigint as weekly_deaths ,
        biweekly_cases::bigint  as biweekly_cases,
        biweekly_deaths::bigint as biweekly_deaths
  from covid.owid_mortes
  