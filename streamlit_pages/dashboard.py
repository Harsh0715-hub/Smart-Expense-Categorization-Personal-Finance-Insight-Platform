import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard(API_BASE_URL):
    st.header("📊 Dashboard")

    # -------- FETCH DATA --------
    summary = requests.get(f"{API_BASE_URL}/summary").json()
    transactions = requests.get(f"{API_BASE_URL}/transactions").json()

    df = pd.DataFrame(transactions)

    # -------- KPI CARDS --------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", summary["income"])
    col2.metric("Expense", summary["expense"])
    col3.metric("Net Savings", summary["income"] - summary["expense"])
    col4.metric("Top Category", summary["top_category"])

    st.divider()

    # -------- PIE CHART --------
    st.subheader("Expense Distribution")

    category_data = df[df["type"] == "debit"].groupby("category")["amount"].sum()

    fig1, ax1 = plt.subplots()
    ax1.pie(category_data, labels=category_data.index, autopct="%1.1f%%")
    st.pyplot(fig1)

    # -------- BAR CHART --------
    st.subheader("Category Spending")

    fig2, ax2 = plt.subplots()
    category_data.plot(kind="bar", ax=ax2)
    st.pyplot(fig2)

    # -------- WEEKLY TREND --------
    st.subheader("Weekly Expense Trend")

    df["date"] = pd.to_datetime(df["date"])
    weekly = df[df["type"] == "debit"].groupby(pd.Grouper(key="date", freq="W"))["amount"].sum()

    fig3, ax3 = plt.subplots()
    weekly.plot(ax=ax3)
    st.pyplot(fig3)

    # -------- TABLE --------
    st.subheader("Transactions")
    st.dataframe(df)