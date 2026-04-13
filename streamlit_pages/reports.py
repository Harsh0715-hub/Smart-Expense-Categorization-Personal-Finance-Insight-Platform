import streamlit as st
import requests
import pandas as pd

def show_reports(API_BASE_URL):
    st.header("📑 Reports")

    try:
        transactions_response = requests.get(f"{API_BASE_URL}/transactions")
        
        if transactions_response.status_code != 200:
            st.error("Failed to fetch data from backend")
            return
        
        transactions = transactions_response.json()
        df = pd.DataFrame(transactions)

        if df.empty:
            st.warning("No transactions uploaded yet. Please upload a CSV file first.")
            return

        # -------- CATEGORY DROPDOWN --------
        if "category" not in df.columns:
            st.error("Missing required column: category")
            return
        
        categories = sorted(df["category"].unique().tolist())
        if not categories:
            st.warning("No categories found in data")
            return
        
        selected_category = st.selectbox("Select Category", categories)

        filtered_df = df[df["category"] == selected_category]

        st.subheader(f"{selected_category} Report")

        st.dataframe(filtered_df)

        # -------- DOWNLOAD BUTTON --------
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv_data,
            file_name=f"{selected_category}_report.csv",
            mime="text/csv"
        )

        # -------- SUMMARY --------
        if "amount" in filtered_df.columns:
            total = filtered_df["amount"].sum()
            st.metric("Total Spending", f"₹ {abs(total):,.2f}")
        else:
            st.error("Missing required column: amount")
            
    except Exception as e:
        st.error(f"Error loading reports: {str(e)}")