import logging
import os
import pandas as pd
import pendulum
import random
import shutil
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
    schedule='*/1 * * * *',  # every minute
    start_date=pendulum.today('UTC').subtract(days=1),
    max_active_runs=1,
    default_args=default_args,
    tags=['data_ingestion'],
)
def my_data_ingestion_dag():

    @task
    def read_data() -> str:
        raw_data_folder = '/Users/macbookair/airflow/raw_data'
        # List the raw_data files
        files = [f for f in os.listdir(raw_data_folder) if f.endswith('.csv') and not f.startswith('.ipynb_checkpoints')]
        if not files:
            logging.warning("No files found in the raw data folder.")
            return ""
        
        random_file = random.choice(files)  # Randomly select one file
        file_path = os.path.join(raw_data_folder, random_file)
        
        logging.info(f"Randomly selected file: {file_path}")
        return file_path  # Return the file path for saving

    @task
    def save_data(file_path: str):
        if not file_path:
            logging.warning("No file path provided. Exiting save_data.")
            return
        
        base_path = '/Users/macbookair/airflow'
        output_folder = os.path.join(base_path, 'good_data')
        os.makedirs(output_folder, exist_ok=True)

        data = pd.read_csv(file_path)  # Read the data
        if not data.empty:
            # Save the processed file with the same name
            output_file = os.path.join(output_folder, os.path.basename(file_path))
            data.to_csv(output_file, index=False)
            logging.info(f"Data saved successfully to {output_file}")
            
            # Move the file to the good_data folder
            destination_path = os.path.join(output_folder, os.path.basename(file_path))
            shutil.move(file_path, destination_path)
            logging.info(f"File moved from {file_path} to {destination_path}")
        else:
            logging.warning("No data to save")

    file_path = read_data()  # Define task dependencies
    save_data(file_path)

data_ingestion_dag = my_data_ingestion_dag()
