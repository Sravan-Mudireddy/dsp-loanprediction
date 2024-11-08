import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
from sqlalchemy import and_
from database import Loan, session
import joblib
from datetime import date

# Load the saved encoder, scaler, and model
le = joblib.load('models/label_encoder.joblib')
scaler = joblib.load('models/scaler.joblib')
model = joblib.load('models/logistic_regression_model.joblib')

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

# Initialize FastAPI app
app = FastAPI()

def preprocess_and_predict(new_data):
    new_data['employment'] = new_data['employment'].str.strip().str.capitalize()
    new_data['employment'] = new_data['employment'].replace({'No': 0, 'Yes': 1})
    new_data['education'] = new_data['education'].str.strip()
    new_data['education'] = new_data['education'].replace({'Graduate': 0, 'Not Graduate': 1})

    x_new = new_data[['dependents', 'education', 'employment', 'annual_income',
                      'loan_amount', 'loan_term', 'cibil_score']]
    x_new_scaled = scaler.transform(x_new)
    predictions = model.predict(x_new_scaled).tolist()

    result = ["Approved" if pred == 0 else "Rejected" for pred in predictions]
    return result

def insert_data(data: LoanPrediction, prediction, source):
    loan_data = Loan(
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
    session.add(loan_data)
    session.commit()

@app.post("/prediction")
async def predict(data: Union[LoanPrediction, MultiPrediction]):
    if isinstance(data, MultiPrediction):
        # Multi-prediction case
        data_dicts = [item.model_dump() for item in data.input]  # Replaced .dict() with .model_dump()
        df = pd.DataFrame(data_dicts)
        output = preprocess_and_predict(df)
        for i in range(len(data.input)):
            insert_data(data.input[i], output[i], 'webapp')
        return {'output': output}

    else:
        # Single prediction case
        df = pd.DataFrame([data.model_dump()])  
        prediction = preprocess_and_predict(df)
        insert_data(data, prediction[0], 'webapp')
        return {'output': prediction[0]}

@app.get("/retrieve")
def retrieve_predictions(start_date: date, end_date: date, source: str):
    query = session.query(Loan).filter(
        and_(
            Loan.created_date >= start_date,
            Loan.created_date <= end_date
        )
    )
    
    
    if source.lower() == "webapp":
        query = query.filter(Loan.source == "webapp")
    elif source.lower() == "scheduled":
        query = query.filter(Loan.source == "scheduled")
    elif source.lower() == "all":
        
        pass
    else:
        return {"error": "Invalid source specified. Please use 'webapp', 'scheduled', or 'all'."}

    results = query.all()
    
    
    response = [
        {
            "id": loan.id,
            "created_date": loan.created_date,
            "created_time": loan.created_time,
            "source": loan.source,
            "dependants": loan.dependants,
            "education": loan.education,
            "employment": loan.employment,
            "annual_income": loan.annual_income,
            "loan_amount": loan.loan_amount,
            "loan_term": loan.loan_term,
            "cibil_score": loan.cibil_score,
            "result": loan.result
        }
        for loan in results
    ]
    
    return response
