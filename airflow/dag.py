import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG('football_analysis',
             schedule = '0 9 * * *',
             start_date = datetime(2024,4,19),
             default_args={"retries":2}
             )

task1 = PythonOperator(task_id = "get_links",
                       python_callable = get_links
                       dag=dag)
