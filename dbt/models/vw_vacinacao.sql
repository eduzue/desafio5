{{ config(materialized='view',
          enabled=true
          ) 
}}
select  date||'_'||replace(location,' ', '_') as chave,
        location ,                           	
        iso_code ,                   
        to_date(date, 'yyyy-mm-dd') as data,
        total_vaccinations::bigint  as total_vaccinations ,               
        people_vaccinated::bigint   as people_vaccinated ,               
        people_fully_vaccinated::bigint   as people_fully_vaccinated,          
        total_boosters::bigint  as total_boosters ,                 
        daily_vaccinations_raw::bigint as daily_vaccinations_raw  ,           
        daily_vaccinations::bigint  as daily_vaccinations    ,             
        total_vaccinations_per_hundred::bigint as total_vaccinations_per_hundred ,    
        people_vaccinated_per_hundred::bigint  as people_vaccinated_per_hundred ,    
        people_fully_vaccinated_per_hundred::bigint  as people_fully_vaccinated_per_hundred  ,
        total_boosters_per_hundred::bigint  as total_boosters_per_hundred ,      
        daily_vaccinations_per_million::bigint as daily_vaccinations_per_million  ,   
        daily_people_vaccinated::bigint  as daily_people_vaccinated  ,         
        daily_people_vaccinated_per_hundred::bigint as daily_people_vaccinated_per_hundred 
from covid.owid_vacinacao