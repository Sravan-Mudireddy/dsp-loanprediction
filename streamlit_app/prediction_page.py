import streamlit as st
import requests
import pandas as pd



st.title("Loan Prediction App")

user_input = st.selectbox("User Input", ("Single Prediction", "Multiple prediction"))

if user_input == "Multiple prediction":
    uploadedFile = st.file_uploader("Upload CSV", type=['.csv','.xlsx'],accept_multiple_files=False,key="fileUploader")
    if uploadedFile is not None:
        df = pd.read_csv(uploadedFile)
        input_data = {'input': df.to_dict(orient='records')}
        st.dataframe(df, hide_index=True)
        file_button = st.button("submit")
        if file_button:
            multi_prediction_url= "http://localhost:8000/multi_prediction"
            response = requests.post(multi_prediction_url, json=input_data)
            if response.status_code == 200:
                predictions = response.json()
                prediction_df = pd.DataFrame(predictions)
                prediction_df = prediction_df.rename(columns={prediction_df.columns[0]: 'Loan_status'})
                result_df = pd.concat([df, prediction_df], axis=1)
                st.dataframe(result_df, hide_index=True)
            else:
                st.write("Error loading API")

else:
    with st.form("user_input", border=True):
        dependents = st.number_input("No of Dependants", min_value=0)
        education = st.selectbox( "Graduation status",
        ("Graduate", "Not Graduate") , index= None, placeholder="Select Graduation status")
        employment = st.selectbox( "Self employed",
        ("Yes", "No") , index= None, placeholder="Select Employment status")
        anual_income = st.number_input("Enter Annual Income", min_value=0)
        loan_amount = st.number_input("Enter Loan Amount", min_value=0)
        loan_term = st.number_input("Enter Term", min_value=3, max_value=100)
        cibil_score = st.number_input("Enter cibil  score", max_value=999)
        button = st.form_submit_button('submit')

    predict_url = "http://localhost:8000/prediction"
    if button:
        input_data = {
            "dependents": dependents,
            "education": education,
            "employment": employment,
            "annual_income": anual_income,
            "loan_amount": loan_amount,
            "loan_term": loan_term,
            "cibil_score": cibil_score
        }
        response = requests.post(predict_url, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.write(f"Your Loan is : **{result['output']}**")
        else:
            st.write("Error loading API")

