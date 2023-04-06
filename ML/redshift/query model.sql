select data, 
	   local,
       mortes_novas,
       diaria_vacinacao,
       diaria_casos,
	fn_covid_ml
		   (data ,
            local,
            diaria_vacinacao,
  			diaria_casos)
         as predictmortes
from covid.total_ml
    where   data >= '2023-01-01'
    and		data <= '2023-05-01'
    and		local = 'Brazil'
order by data ;