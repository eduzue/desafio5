SELECT
      ROUND(AVG(POWER(( atual - case when predictmortes < 0 then 0 else predictmortes end ),2)),2) mse
    , ROUND(SQRT(AVG(POWER(( atual - case when predictmortes < 0 then 0 else predictmortes end ),2))),2) rmse
FROM  
    (SELECT
           data
         , mortes_novas AS atual
         , fn_covid_ml
		   (data ,
            local,
            diaria_vacinacao,
  			diaria_casos)
         as predictmortes
     FROM  covid.total_ml
     where local = 'Brazil'
     and data >= '2023-01-01');