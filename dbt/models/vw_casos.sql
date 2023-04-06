{{ config(materialized='view',
          enabled=true
          ) 
}}

 select data||'_'||replace(localizacao,' ','_') as chave,
        to_date(data, 'yyyy-mm-dd') as data, 
        localizacao,
        casos::bigint as casos
from covid.owid_casos
