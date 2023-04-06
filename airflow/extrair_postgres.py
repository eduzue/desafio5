import boto3
import os
import pandas as pd
from dotenv import load_dotenv

from sqlalchemy import create_engine

nome_csv_postgres = 'dadospostgres.csv'
nome_parquet_postgres = 'dadospostgres.parquet'
nome_bucket = 'desafio5'
nome_pasta_postgres = 'dadospostgres'

load_dotenv()

ENDPOINT="covid.cnotjz24wwh2.us-east-1.rds.amazonaws.com"
PORT="5432"
REGION="us-east-1"
DBNAME="fiap"

v_passwd=os.getenv("PASSWORD_PG")
v_user=os.getenv("USER_PG")

#Criar a conexão
engine = create_engine("postgresql+psycopg2://"+v_user+":"+v_passwd+"@"+ENDPOINT+":"+PORT+"/"+DBNAME)

sql = "SELECT * from fiap.covid"
#Fazer o SQL e colocar no dataframe df, utilizando o read_sql_query do pandas
df = pd.read_sql_query(sql, engine)

#renomear a primeira coluna, que está vazia
#df.columns.values[0] = 'linha'
#print(df)
#Sem índice, (número da linha)
df.to_csv(nome_csv_postgres,sep=';',index=False)
#print(df['critical_condition'].fillna(0))
#print(df['critical_condition'])
#df = df.replace({'',np.nan})
#mostrar os registros com o campo critical_condition nulo
#print(df['critical_condition'].isnull())
#substituir abaixo o '' por 0. substituir todas as vírgulas por nada.
#df['critical_condition'] = df['critical_condition'].fillna(0).replace('',0).replace(',','').astype('float')
df['critical_condition'] = df['critical_condition'].astype('str')
#print(df['critical_condition'])

df.to_parquet(nome_parquet_postgres, index=False)


#gets the credentials from .aws/credentials
session = boto3.Session()
client_postgres = session.client('rds')
client_s3 = boto3.client('s3')

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('desafio5')

#enviar o arquivo gerado
client_s3.upload_file(nome_csv_postgres, nome_bucket, nome_pasta_postgres+'/'+nome_csv_postgres)

client_s3.upload_file(nome_parquet_postgres, nome_bucket, nome_pasta_postgres+'/'+nome_parquet_postgres)

#listar os objetos na pasta 
for object_summary in my_bucket.objects.filter(Prefix="dadospostgres"+"/"):
    print(object_summary.key)

#conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=v_user, password=v_passwd, sslrootcert="SSLCERTIFICATE")
#dados = sqlio.read_sql_query(sql,conn)
#print(dados)