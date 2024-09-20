Loan Approval Prediction Web Application and Monitoring System
This repository contains the source code, Airflow DAGs, and documentation for a comprehensive Loan Approval Prediction Web Application and Monitoring System. The system facilitates loan approval predictions through a user-friendly web interface and includes components for data ingestion, validation, scheduled predictions, and monitoring of both data flow and model performance.
Project Structure
This project is structured into several key components, including a web application, a model-serving API, an automated data ingestion pipeline, prediction jobs, and data quality monitoring tools. Below is an overview of the key components:
1. Web Application, API, and Database
Web Application
The web application is built using Streamlit, providing an intuitive and user-friendly interface for loan approval predictions. Users can interact with the app for both individual and batch predictions.
Prediction Page:
Users can manually input loan application data or upload CSV files for batch predictions.
The system provides real-time loan approval results for the submitted data.
Past Predictions Page:
Users can view historical predictions, filtered by date range or input source (manual vs. batch).
Displays all relevant prediction details and features used.
API (Model Service)
The model prediction service is built using FastAPI, providing an efficient and scalable backend API to serve the prediction model.
Endpoints:
/predict: Accepts loan application data and returns predictions (supports both single and batch predictions).
/past-predictions: Retrieves previous predictions from the database, including all input features and corresponding results.
Database
The historical predictions are stored in a PostgreSQL database, which allows for querying and analysis of past predictions via the API or web app interface.
2. Data Issue Generation Notebook
A Jupyter Notebook is included to simulate and introduce common data quality issues in the raw loan application dataset. The notebook helps in testing and validating the system’s ability to handle data problems such as:
Missing Values: Introduces missing data in required fields (e.g., loan amount, applicant income).
Outliers: Inserts outliers in numeric columns (e.g., unusually high or low loan amounts).
Data Type Mismatches: Creates incorrect data types or feature value mismatches (e.g., categorical features having numeric values).
This is useful for testing the robustness of the data ingestion and validation process.
3. Data Generation Script
The loan_approval_splitting_files.py script is responsible for simulating the flow of incoming loan applications by generating new loan application data and saving it as CSV files into the raw-data folder.
Functionality:
Randomly generates loan application data in CSV format, mimicking real-time submission of loan applications.
This data will be processed in later stages by the data ingestion pipeline.
4. Data Ingestion Pipeline
The data ingestion pipeline is managed through an Apache Airflow DAG, which is responsible for moving and validating new data files.
Airflow DAG: Data Ingestion
This DAG handles the ingestion of new loan application data into the system. It validates the data and ensures only valid datasets are processed further.
Tasks:
read-data: Reads a randomly selected file from the raw-data folder.
validate-and-move: Validates the integrity of the file (e.g., checks for missing values, data type mismatches) and moves it to the good-data folder for further processing.
The ingestion pipeline ensures that only data conforming to predefined standards is sent for prediction.
5. Prediction Job Pipeline
This pipeline is another Airflow DAG that automates the prediction process based on newly ingested data.
Airflow DAG: Prediction Job
The prediction job is responsible for detecting new data files, sending the data for predictions, and storing the results in the database.
Tasks:
check_for_new_data: Periodically checks the good-data folder for new files. If no new files are found, the task is skipped.
make_predictions: Sends the newly found data to the model service API, retrieves predictions, and stores them in the database for future reference.
This pipeline ensures predictions are made on newly ingested data in an automated manner.
Installation
Prerequisites
To set up the system locally, ensure you have the following dependencies installed:
Python 3.7+
PostgreSQL
Docker (optional but recommended for easier deployment)
Airflow
Setup Instructions
Clone the repository:
bash
git clone https://github.com/your-username/loan_approval_prediction.git
cd loan_approval_prediction
Create and activate a virtual environment:
bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`

Install dependencies:
pip install -r requirements.txt
 
Start the FastAPI server (Model Service):
uvicorn app.main:app –reload
 
Start the Streamlit web application:
streamlit run app/webapp.py
 
Usage
Web Application
Prediction Page: Access the prediction page at http://127.0.0.1:8501 (Streamlit default port).
Input loan application data manually or upload a CSV file for batch predictions.
Click "Predict" to receive the loan approval prediction results.
Past Predictions Page: Access via the same Streamlit app to view historical predictions, filtered by date or data source.
Model Service (API)
Make Predictions:
Send a POST request to /predict with the required loan application features in JSON or CSV format.
Example request:
bash
curl -X 'POST' \
'http://127.0.0.1:8000/predict' \
 -H 'Content-Type: application/json' \
 -d '{"loan_amount": 10000, "income": 50000, ...}'
 
Retrieve Past Predictions:
Send a GET request to /past-predictions to retrieve a list of all past predictions.
Data Ingestion and Prediction Jobs
Airflow DAGs:
Access the Airflow UI to trigger or monitor the data ingestion and prediction jobs.
Both DAGs (data_ingestion_dag and prediction_job_dag) can be run on a scheduled basis or triggered manually via the Airflow interface.

Contributors
1)Sravan Kumar Mudireddy
2)Niveda Nadarassin
3)Madhukesava Natava
4)Thierry Celestin Legue Doho
5)Ananya Gownivari Ravindrareddy
 
Support
For any support or inquiries regarding this project, please contact us.

 