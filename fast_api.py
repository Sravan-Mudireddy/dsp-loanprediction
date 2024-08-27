import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import Loan, session
from datetime import date
from sqlalchemy import and_
import joblib


class LoanPrediction(BaseModel):
    dependents: int
    education: str
    employment: str
    annual_income: int
    loan_amount: int
    loan_term: int
    cibil_score: int


class MultiPrediction(BaseModel):
    input: List[LoanPrediction]


# Load the saved encoder, scaler, and model
le = joblib.load('models/label_encoder.joblib')
scaler = joblib.load('models/scaler.joblib')
model = joblib.load('models/logistic_regression_model.joblib')

def preprocess_and_predict(new_data):

    new_data['employment'] = new_data['employment'].str.strip().str.capitalize()
    new_data['employment'] = new_data['employment'].replace({'No': 0, 'Yes': 1})
    new_data['education'] = new_data['education'].str.strip()
    new_data['education'] = new_data['education'].replace({'Graduate': 0, 'Not Graduate': 1})


    x_new = new_data[['dependents', 'education', 'employment', 'annual_income',
                      'loan_amount', 'loan_term', 'cibil_score']]
    x_new_scaled = scaler.transform(x_new)
    # Make predictions
    predictions = model.predict(x_new_scaled).tolist()

    result = ["Approved" if pred == 0 else "Rejected" for pred in predictions]

    return result


def predict_csv_input(data):
    output = ['Rejected' for _ in range(len(data.input))]
    return output


def insert_data(data: LoanPrediction, prediction, source):
    data = Loan(
        source=source,
        dependants=data.dependents,
        education=data.education,
        employment=data.employment,
        annual_income=data.annual_income,
        loan_amount=data.loan_amount,
        loan_term=data.loan_term,
        cibil_score=data.cibil_score,
        result=prediction
    )
    session.add(data)
    session.commit()


app = FastAPI()


@app.post("/prediction")
def get_prediction(data: LoanPrediction):
    df = pd.DataFrame([data.dict()])
    prediction = preprocess_and_predict(df)
    insert_data(data,prediction[0], 'webapp')
    return {'output': prediction[0]}


@app.post("/multi_prediction")
def get_multi_prediction(data: MultiPrediction):
    data_dicts = [item.dict() for item in data.input]
    df = pd.DataFrame(data_dicts)
    output = preprocess_and_predict(df)
    for i in range(len(data.input)):
        insert_data(data.input[i], output[i], 'webapp')
    return {'output': output}


@app.get("/retrieve")
def retrieve_predictions(start_date: date, end_date: date, source):
    query = session.query(Loan).filter(
        and_(
            Loan.created_date >= start_date,
            Loan.created_date <= end_date
        )
    )

    if source and source != "All":
        query = query.filter(Loan.source == source.lower())

    results = query.all()

    return results