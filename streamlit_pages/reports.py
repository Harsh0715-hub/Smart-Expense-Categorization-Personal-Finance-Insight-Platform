import streamlit as st
import requests
import pandas as pd

def show_reports(API_BASE_URL):
    st.header("📑 Reports")

    transactions = requests.get(f"{API_BASE_URL}/transactions").json()
    df = pd.DataFrame(transactions)

    # -------- CATEGORY DROPDOWN --------
    categories = df["category"].unique().tolist()
    selected_category = st.selectbox("Select Category", categories)

    filtered_df = df[df["category"] == selected_category]

    st.subheader(f"{selected_category} Report")

    st.dataframe(filtered_df)

    # -------- SUMMARY --------
    total = filtered_df["amount"].sum()
    st.metric("Total Spending", total)