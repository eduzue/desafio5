#import sys
#import subprocess
#import os
#
#
#sys.path.insert(0,'/root/bin:/home/airflow/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin')
#print(sys.path)
#os.environ["AIRFLOW_CTX_DAG_OWNER"] = "airflow"
#usuario=os.getenv("AIRFLOW_CTX_DAG_OWNER", None)
#print("usuário")
#print(usuario)
#os.chdir("/opt/airflow/dags/dbt/covid/")
#subprocess.call('dbt build', shell=True)

#cria e executa de forma recursiva os modelos do dbt 
from datetime import datetime, timedelta
import json
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta, datetime
from airflow.utils.dates import days_ago


dag = DAG(
    dag_id="dbt_dag",
    default_args={
        'owner': 'airflow',
        'start_date': datetime.now(),
        'end_date': datetime.now() + timedelta(days=1, hours=3),
        'depends_on_past': False,
        'run_as_user': 'airflow',
    }, 
    schedule='@once',
    dagrun_timeout=timedelta(minutes=20000),
    start_date = datetime.now()
)


def load_manifest():
    local_filepath = "/opt/airflow/dags/dbt/covid/target/manifest.json"
    with open(local_filepath) as f:
        data = json.load(f)
    return data


def make_dbt_task(node, dbt_verb):
    """Returns an Airflow operator either run and test an individual model"""
    DBT_DIR = "/opt/airflow/dags/dbt/covid"
    GLOBAL_CLI_FLAGS = "--no-write-json"
    model = node.split(".")[-1]

    if dbt_verb == "run":
        dbt_task = BashOperator(
            task_id=node,
            bash_command=f"""
            cd {DBT_DIR} &&
            /usr/local/bin/dbt {GLOBAL_CLI_FLAGS} {dbt_verb} --target prod --models {model}
            """,
            dag=dag,
        )

    elif dbt_verb == "test":
        node_test = node.replace("model", "test")
        dbt_task = BashOperator(
            task_id=node_test,
            bash_command=f"""
            cd {DBT_DIR} &&
            dbt {GLOBAL_CLI_FLAGS} {dbt_verb} --target prod --models {model}
            """,
            dag=dag,
        )

    return dbt_task


data = load_manifest()

dbt_tasks = {}
for node in data["nodes"].keys():
    if node.split(".")[0] == "model":
        node_test = node.replace("model", "test")

        dbt_tasks[node] = make_dbt_task(node, "run")
        dbt_tasks[node_test] = make_dbt_task(node, "test")

for node in data["nodes"].keys():
    if node.split(".")[0] == "model":
        # Set dependency to run tests on a model after model runs finishes
        node_test = node.replace("model", "test")
        dbt_tasks[node] >> dbt_tasks[node_test]

        # Set all model -> model dependencies
        for upstream_node in data["nodes"][node]["depends_on"]["nodes"]:
            upstream_node_type = upstream_node.split(".")[0]
            if upstream_node_type == "model":
                dbt_tasks[upstream_node] >> dbt_tasks[node]

