create model covid_ml from (
    select  data ,
            local,
            diaria_vacinacao,
  			diaria_casos,
  		    mortes_novas
    from    covid.total_ml
    where   data <= '2023-02-01'
)
TARGET mortes_novas
FUNCTION fn_covid_ml
IAM_ROLE default 
PROBLEM_TYPE regression
SETTINGS ( S3_BUCKET 'ml-redshift-desafio-5'
); 