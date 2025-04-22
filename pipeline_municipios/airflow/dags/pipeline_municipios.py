from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Funções para executar cada script Python individualmente
def run_download_populacao():
    subprocess.run(["python", "download_populacao.py"])

def run_load_populacao():
    subprocess.run(["python", "load_populacao.py"])

def run_load_leitos():
    subprocess.run(["python", "load_leitos.py"])

def run_load_enem():
    subprocess.run(["python", "load_enem.py"])

def run_testes_qualidade():
    subprocess.run(["python", "testes_qualidade.py"])

# Definindo o DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 22),
    'retries': 1,
}

with DAG(
    'pipeline_municipios',
    default_args=default_args,
    description='Pipeline completo para carga de dados municipais',
    schedule=None,  # O cronograma pode ser ajustado, ou setar como None para execução manual
    catchup=False,
) as dag:

    # Definindo as tarefas do DAG
    task_download_populacao = PythonOperator(
        task_id='download_populacao',
        python_callable=run_download_populacao,
    )

    task_load_populacao = PythonOperator(
        task_id='load_populacao',
        python_callable=run_load_populacao,
    )

    task_load_leitos = PythonOperator(
        task_id='load_leitos',
        python_callable=run_load_leitos,
    )

    task_load_enem = PythonOperator(
        task_id='load_enem',
        python_callable=run_load_enem,
    )

    task_testes_qualidade = PythonOperator(
        task_id='testes_qualidade',
        python_callable=run_testes_qualidade,
    )

    # Definindo a sequência de execução
    task_download_populacao >> task_load_populacao >> task_load_leitos >> task_load_enem >> task_testes_qualidade
