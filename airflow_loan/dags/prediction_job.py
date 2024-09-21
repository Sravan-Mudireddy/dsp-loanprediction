import logging
import os
import pendulum
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import requests  # To send requests to the prediction model service

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'email_on_failure': False,
    'email_on_retry': False,
}

@dag(
    dag_id='predict_dag',
    description='A DAG to check for new data and make predictions',
    schedule='*/2 * * * *',  # Every 2 minutes
    start_date=pendulum.today('UTC').subtract(days=1),
    max_active_runs=1,
    default_args=default_args,
    tags=['prediction'],
)
def prediction_dag():

    # Task 1: Check for new data in good_data folder
    @task
    def check_for_new_data() -> str:
        good_data_folder = '/Users/macbookair/airflow/good_data/test'
        files = [f for f in os.listdir(good_data_folder) if f.endswith('.csv')]

        if not files:
            logging.info("No new files found in the test folder.")
            return ""  # If no new files, we return an empty string
        
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(good_data_folder, f)))
        file_path = os.path.join(good_data_folder, latest_file)
        logging.info(f"Latest file found for prediction: {file_path}")
        return file_path

    # Task 2: Make predictions on new data
    @task
    def make_predictions(file_path: str):
        if not file_path:
            logging.warning("No file path provided. Skipping prediction.")
            return
        
        # Simulate a request to the prediction API (replace with actual API endpoint)
        prediction_url = "http://model_service/predict"  # Replace with actual URL
        data = pd.read_csv(file_path)
        response = requests.post(prediction_url, json=data.to_dict(orient='records'))

        if response.status_code == 200:
            logging.info(f"Predictions successful for {file_path}")
        else:
            logging.error(f"Prediction failed for {file_path}. Status code: {response.status_code}")

    file_path = check_for_new_data()
    make_predictions(file_path)

# Instantiate the prediction DAG
prediction_dag = prediction_dag()
