Here's a complete `README.md` file for your **Loan Approval Prediction Web Application and Monitoring System**, following the structure and content style of the provided example.

---

# Loan Approval Prediction Web Application and Monitoring System

This repository contains the source code, Airflow DAGs, and documentation for a comprehensive **Loan Approval Prediction Web Application and Monitoring System**. The system enables loan approval predictions, visualizes past predictions, serves predictions via an API, automates data ingestion with quality checks, schedules predictions, and monitors data and model performance using Grafana dashboards.

## Project Structure

The project is structured into several components:

### Web Application

#### **Prediction Page**
- Allows users to make single or batch predictions by filling out a form or uploading a CSV file.
- Uses a model API service for predictions, providing real-time feedback.
  
#### **Past Predictions Page**
- Enables users to view historical predictions with options to filter by date range and input source (manual or batch upload).

### Model Service (API)

- **Endpoints**:
  - `/predict`: Accepts loan application data for single or batch predictions.
  - `/past-predictions`: Retrieves past predictions, including input features and prediction results.
  
### Database

- Uses **PostgreSQL** to store predictions and data quality logs. This allows access to historical prediction data and data quality insights for monitoring.

### Data Ingestion Job

- **Continuous Data Ingestion**: Simulates a continuous data flow by ingesting new loan applications at regular intervals.
- **Data Quality Validation**: Automatically validates ingested data quality, checking for missing values, data type mismatches, and outliers.
- **Error Handling**: Introduces data errors for testing and logs quality issues for future reference.

### Prediction Job

- **Scheduled Predictions**: Runs predictions on newly ingested data at regular intervals, storing prediction results in the database.

### Monitoring Dashboards

- **Ingested Data Monitoring Dashboard**: Helps data operations teams monitor data quality issues in real time.
- **Data Drift and Prediction Issues Dashboard**: Allows ML engineers and data scientists to detect data drift, model degradation, and other issues impacting prediction accuracy.

## Installation

### Prerequisites
- Python 3.7+
- PostgreSQL
- Docker (optional for containerized deployment)
- Apache Airflow
- Grafana

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/loan_approval_prediction.git
   cd loan_approval_prediction
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**
   - Install PostgreSQL and create a database.
   - Update the `DATABASE_URL` in the `.env` file with your PostgreSQL connection string.

5. **Run database migrations**
   - Use Alembic to run migrations for setting up the initial database schema:
     ```bash
     alembic upgrade head
     ```

6. **Start the FastAPI model service**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Start the Streamlit web application**
   ```bash
   streamlit run app/webapp.py
   ```

8. **Set up Airflow**
   - Follow the [official Airflow installation guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html).
   - Place the `data_ingestion_dag` and `prediction_job_dag` in the Airflow `dags/` folder.
   - Start the Airflow scheduler and web server.

9. **Set up Grafana for monitoring**
   - Install Grafana and create a new dashboard.
   - Add panels to track data ingestion, prediction performance, and error logs.
   - Configure Grafana to connect to PostgreSQL for real-time monitoring.

## Usage

### Web Application

1. **Prediction Page**: 
   - Access the prediction page at `http://127.0.0.1:8501`.
   - Submit loan application data manually or upload a CSV file for batch predictions.
   - Receive prediction results directly on the web application.

2. **Past Predictions Page**:
   - Access the historical predictions page to view and filter past predictions by date or input type.

### Model Service (API)

- **Make predictions**:
  ```bash
  curl -X POST 'http://127.0.0.1:8000/predict' -H 'Content-Type: application/json' -d '{"loan_amount": 10000, "income": 50000, ...}'
  ```
- **Retrieve past predictions**:
  ```bash
  curl -X GET 'http://127.0.0.1:8000/past-predictions'
  ```

### Data Ingestion and Prediction Jobs

- **Airflow DAGs**: Access Airflow UI to monitor or trigger the `data_ingestion_dag` and `prediction_job_dag`.
  
  - **Data Ingestion DAG**:
    - Ingests new loan applications from `raw-data` and validates them for data quality.
    - Saves valid data to the `good-data` folder for further processing.

  - **Prediction Job DAG**:
    - Automatically predicts on validated data in `good-data`.
    - Archives processed files after predictions are stored in the database.

### Monitoring Dashboards (Grafana)

- **Access Grafana dashboards** to monitor:
  - **Ingested Data Quality**: Tracks missing values, data type mismatches, and outliers in ingested data.
  - **Prediction Accuracy**: Visualizes model performance metrics over time, helping detect potential data drift.
  - **Error Logs**: Logs errors and issues from the ingestion pipeline for proactive issue management.

## Contributors

- Sravan Kumar Mudireddy
- Niveda Nadarassin
- Madhukesava Natava
- Thierry Celestin Legue Doho
- Ananya Gownivari Ravindrareddy

## Support

For support or inquiries related to the project, please contact us.

## Acknowledgements

- Streamlit
- FastAPI
- PostgreSQL
- Apache Airflow
- Grafana
- Great Expectations

---