from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from datetime import datetime

default_args = {
    'owner': 'smartfarm',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='smartfarm_etl',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 5, 1),
    catchup=True,
) as dag:

    generate = BashOperator(
        task_id='generate_synthetic_data',
        bash_command='python /opt/scripts/generate_data.py --out /data/input/generator_output.jsonl --count 12000 --anomaly-rate 0.03'
    )

    wait = BashOperator(
        task_id='wait_for_ingest',
        bash_command='sleep 10'
    )

    # placeholder: in a real setup NiFi would pick up /data/input and route to Postgres/Elasticsearch
    verify = BashOperator(
        task_id='verify_generation',
        bash_command='ls -l /data/input || true'
    )

    generate >> wait >> verify
