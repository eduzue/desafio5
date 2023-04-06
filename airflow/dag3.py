import airflow
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, datetime
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

with DAG(
    'baixa_dados_3',
    default_args={
        'owner': 'airflow',
        'start_date': airflow.utils.dates.days_ago(1),
        'end_date': datetime.now(),
        'depends_on_past': False,
        
    }, 
    schedule_interval='@once',
    dagrun_timeout=timedelta(minutes=20000),
    start_date = airflow.utils.dates.days_ago(1)

) as dag:
    download_data = BashOperator(
        task_id='download_data', 
        bash_command='/usr/local/bin/python /opt/airflow/dags/dados.py',
    )
    sent_to_redshift = BashOperator(
        task_id='send_to_redshift', 
        bash_command='/usr/local/bin/python /opt/airflow/dags/redshift.py',
    )
    dbt_run = BashOperator(
    task_id='dbt_run', 
    bash_command='/usr/local/bin/python /opt/airflow/dags/execute_dbt.py',
    )
    download_data >> sent_to_redshift >> dbt_run