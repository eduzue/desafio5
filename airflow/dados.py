import requests
import pandas as pd
from io import StringIO
import boto3
import os

from dotenv import load_dotenv

load_dotenv()


v_access=os.getenv("ACCESS_KEY_ID")
v_secret=os.getenv("SECRET_KEY")

client_s3 = boto3.client('s3',
						aws_access_key_id=v_access,
                        aws_secret_access_key=v_secret,
                        region_name='us-east-1')

s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket('desafio5')
nome_bucket = 'desafio5'


#Vacina
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
response = requests.get(url)

csvstring = StringIO(response.text)

if response.status_code == 200:
    dfvacina = pd.read_csv(csvstring, sep=',')
    #print(dfvacina)
    #define buffer do csv em uma string de memória
    dfvacina.to_parquet('vacinacao.parquet',index=False, compression='gzip')
    client_s3.upload_file(r'vacinacao.parquet', nome_bucket, 'owid'+'/'+'vacinacao.parquet')

    #s3_resource.Object(nome_bucket, 'vacinacoes.csv').put(Body=csv_buffer.getvalue())
dfvacina.info()


#mortes
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/cases_deaths/full_data.csv'
response = requests.get(url)

csvstring = StringIO(response.text)

if response.status_code == 200:
    dfmortes = pd.read_csv(csvstring, sep=',')
    #print(dfmortes)
    #define buffer do csv em uma string de memória
    dfmortes.to_parquet('mortes.parquet',index=False , compression='gzip')
    client_s3.upload_file(r'mortes.parquet', nome_bucket, 'owid'+'/'+'mortes.parquet')

    #s3_resource.Object(nome_bucket, 'vacinacoes.csv').put(Body=csv_buffer.getvalue())
dfmortes.info()

#casos
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/cases_deaths/total_cases.csv'
response = requests.get(url)

csvstring = StringIO(response.text)

if response.status_code == 200:
    dfcasos = pd.read_csv(csvstring, sep=',')
    #print(dfcasos)
    ##define buffer do csv em uma string de memória
    df3= dfcasos.copy()
    df3.set_index(df3.columns[0], inplace=True)
    df3 = df3.stack().reset_index()
    df3.columns=['date', 'localizacao', 'valor']
    df3.astype(str)
    df3.to_parquet('casos.parquet',index=False , compression='gzip')
    client_s3.upload_file(r'casos.parquet', nome_bucket, 'owid'+'/'+'casos.parquet')

    #s3_resource.Object(nome_bucket, 'vacinacoes.csv').put(Body=csv_buffer.getvalue())
#dfcasos.info()


#casos por milhão
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/cases_deaths/total_deaths_per_million.csv'
response = requests.get(url)

csvstring = StringIO(response.text)

if response.status_code == 200:
    dfcasospm = pd.read_csv(csvstring, sep=',')
    #print(dfcasospm)
    #
    df2 = dfcasospm.copy()
    df2.set_index(df2.columns[0], inplace=True)
    df2 = df2.stack().reset_index()
    df2.columns=['date', 'localizacao', 'valor']
    #define buffer do csv em uma string de memória
    df2.to_parquet('casospm.parquet',index=False , compression='gzip')
    df3.astype(str)
    client_s3.upload_file(r'casospm.parquet', nome_bucket, 'owid'+'/'+'casospm.parquet')

    #s3_resource.Object(nome_bucket, 'vacinacoes.csv').put(Body=csv_buffer.getvalue())

#df2.info()


