import logging
import os
import pandas as pd
import pendulum
import random
from airflow.decorators import dag, task

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'email_on_failure': False,
    'email_on_retry': False,
}

@dag(
    dag_id='data_ingestion_dag',
    description='A DAG for reading and saving data',
    schedule='0 */1 * * *',  # every hour
    start_date=pendulum.today('UTC').subtract(days=1),
    max_active_runs=1,
    default_args=default_args,
    tags=['data_ingestion'],
)
def my_data_ingestion_dag():

    @task
    def read_data() -> pd.DataFrame:
        raw_data_folder = '/Users/macbookair/airflow/raw_data'
        
        # List the raw_data files
        files = [f for f in os.listdir(raw_data_folder) if f.endswith('.csv') and not f.startswith('.ipynb_checkpoints')]
        
        if not files:
            logging.warning("No files found in the raw data folder.")
            return pd.DataFrame()

        # Randomly select one file
        random_file = random.choice(files)
        file_path = os.path.join(raw_data_folder, random_file)
        
        logging.info(f"Randomly selected file: {file_path}")
        
        # Read the selected file
        data = pd.read_csv(file_path)
        logging.info(f"Rows read from {file_path}: {len(data)}")
        
        return data

    @task
    def save_data(data: pd.DataFrame):
        base_path = '/Users/macbookair/airflow'
        output_folder = os.path.join(base_path, 'good_data')
        os.makedirs(output_folder, exist_ok=True)

        if not data.empty:
            output_file = os.path.join(output_folder, 'processed_data.csv')
            data.to_csv(output_file, index=False)
            logging.info(f"Data saved successfully to {output_file}")
        else:
            logging.warning("No data to save")

    # Define task dependencies
    data = read_data()
    save_data(data)

data_ingestion_dag = my_data_ingestion_dag()
