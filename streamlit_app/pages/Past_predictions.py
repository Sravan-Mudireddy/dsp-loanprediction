import streamlit as st
import requests
import pandas as pd

# Past Predictions Section
st.header('Past Predictions')
start_date = st.date_input("Start Date", value=None)
end_date = st.date_input("End Date", value=None)
selected = st.selectbox("Choose Source", ("webapp", "Scheduled", "All"))
button = st.button('Retrieve')

if button:
    url = "http://127.0.0.1:8000/retrieve"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "source": selected
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        predictions = response.json()
        df = pd.DataFrame(predictions)

        # Reorder columns for display
        column_order = [
            'id', 'created_date', 'created_time', 'source', 'dependants', 'education', 'employment',
            'annual_income', 'loan_amount', 'loan_term', 'cibil_score', 'result'
        ]
        df = df.reindex(columns=column_order)
        st.dataframe(df, hide_index=True)

        # Displaying a single unified statistics table
        if not df.empty:
            st.subheader("Statistics of Retrieved Data")

            # Calculate statistics for numerical fields
            numeric_stats = df[['annual_income', 'loan_amount', 'loan_term', 'cibil_score']].describe().loc[
                ['count', 'mean', 'std', 'min', 'max']].T
            numeric_stats.reset_index(inplace=True)
            numeric_stats.columns = ["Metric", "Count", "Mean", "Std", "Min", "Max"]

            # Calculate loan status distribution
            loan_status_counts = df['result'].value_counts()
            loan_status_data = {
                "Metric": ["Loan Status - Approved", "Loan Status - Rejected"],
                "Count": [loan_status_counts.get("Approved", 0), loan_status_counts.get("Rejected", 0)],
                "Mean": ["-", "-"],
                "Std": ["-", "-"],
                "Min": ["-", "-"],
                "Max": ["-", "-"]
            }
            loan_status_df = pd.DataFrame(loan_status_data)

            # Combine numerical stats and loan status into a single table
            combined_stats = pd.concat([numeric_stats, loan_status_df], ignore_index=True)

            # Display the final combined statistics table
            st.table(combined_stats)

        else:
            st.write("No data available for the selected period or source.")

    else:
        st.error("Failed to retrieve predictions")
