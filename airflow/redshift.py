import redshift_connector



conn = redshift_connector.connect(
     host='redshift-cluster-1.cibczfddbdrt.us-east-1.redshift.amazonaws.com',
     database='dev',
     port=5439,
     user='awsuser',
     password='61A8!j(5Wq'
  )

cursor = conn.cursor()

cursor.execute("drop table covid.owid_casospm cascade;") 
cursor.execute("drop table covid.owid_casos cascade;")
cursor.execute("drop table covid.owid_vacinacao cascade;")
cursor.execute("drop table covid.owid_mortes cascade;")

cursor.execute(" create table if not exists covid.owid_casospm (  " + \
               "     data  varchar not null,                      " + \
               "     localizacao varchar not null,                " + \
               "     casos       float                            " + \
               " );                                               "
                )

cursor.execute(" create table if not exists covid.owid_casos (  " + \
               "     data  varchar not null,                    " + \
               "     localizacao varchar not null,              " + \
               "     casos       float                          " + \
               " );                                             "
                )

cursor.execute(" create table if not exists covid.owid_vacinacao (" + \
               " location  VARCHAR NOT NULL,                      " + \
               " iso_code  VARCHAR NOT NULL,                      " + \
               " date      VARCHAR NOT NULL,                      " + \
               " total_vaccinations  FLOAT,                       " + \
               " people_vaccinated   FLOAT,                       " + \
               " people_fully_vaccinated  FLOAT,                  " + \
               " total_boosters    FLOAT,                         " + \
               " daily_vaccinations_raw  FLOAT,                   " + \
               " daily_vaccinations    FLOAT,                     " + \
               " total_vaccinations_per_hundred FLOAT,            " + \
               " people_vaccinated_per_hundred  FLOAT,            " + \
               " people_fully_vaccinated_per_hundred   FLOAT,     " + \
               " total_boosters_per_hundred   FLOAT,              " + \
               " daily_vaccinations_per_million  FLOAT,           " + \
               " daily_people_vaccinated   FLOAT,                 " + \
               " daily_people_vaccinated_per_hundred FLOAT);      " 
                )  

cursor.execute("  create table if not exists covid.owid_mortes (" + \
              "  date  VARCHAR NOT NULL," + \
              "  location  VARCHAR NOT NULL,                   " + \
              "  new_cases      FLOAT,                         " + \
              "  new_deaths       FLOAT,                       " + \
              "  total_cases      FLOAT,                       " + \
              "  total_deaths     FLOAT,                       " + \
              "  weekly_cases     FLOAT,                       " + \
              "  weekly_deaths    FLOAT,                       " + \
              "  biweekly_cases   FLOAT,                       " + \
              "  biweekly_deaths  FLOAT                        " + \
              "  );                                            "
                )

conn.commit()


cursor.execute("copy covid.owid_casospm from 's3://desafio5/owid/casospm.parquet' iam_role 'arn:aws:iam::343055481759:role/service-role/AmazonRedshift-CommandsAccessRole-20230303T094804' format parquet ;")
cursor.execute("copy covid.owid_casos from 's3://desafio5/owid/casos.parquet' iam_role 'arn:aws:iam::343055481759:role/service-role/AmazonRedshift-CommandsAccessRole-20230303T094804' format parquet ;")
cursor.execute("copy covid.owid_vacinacao from 's3://desafio5/owid/vacinacao.parquet' iam_role 'arn:aws:iam::343055481759:role/service-role/AmazonRedshift-CommandsAccessRole-20230303T094804' format parquet ;")
cursor.execute("copy covid.owid_mortes from 's3://desafio5/owid/mortes.parquet' iam_role 'arn:aws:iam::343055481759:role/service-role/AmazonRedshift-CommandsAccessRole-20230303T094804' format parquet ;")

print("Casos por milhão:")
cursor.execute("select count(*) from covid.owid_casospm;")
print(cursor.fetchall())
print("Casos novos:")
cursor.execute("select count(*) from covid.owid_casos;")
print(cursor.fetchall())
print("Vacinacao:")
cursor.execute("select count(*) from covid.owid_vacinacao;")
print(cursor.fetchall())
print("Mortes:")
cursor.execute("select count(*) from covid.owid_mortes;")
print(cursor.fetchall())

#cursor.execute("copy covid.atu from 's3://desafio5/dadosatuparquet/dados' iam_role 'arn:aws:iam::343055481759:role/service-role/AmazonRedshift-CommandsAccessRole-20230303T094804' format parquet ;")
#Caso for csv na linha de cima: FORMAT CSV DELIMITER ';' ignoreheader 1
#cursor.execute("select * from covid.atu")
#print(cursor.fetchall())

conn.commit()