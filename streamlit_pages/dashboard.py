import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard(API_BASE_URL):
    st.header("📊 Dashboard")

    try:
        # -------- FETCH DATA --------
        summary_response = requests.get(f"{API_BASE_URL}/summary")
        transactions_response = requests.get(f"{API_BASE_URL}/transactions")
        
        if summary_response.status_code != 200 or transactions_response.status_code != 200:
            st.error("Failed to fetch data from backend")
            return
        
        summary = summary_response.json()
        transactions = transactions_response.json()

        df = pd.DataFrame(transactions)
        
        if df.empty:
            st.warning("No transactions uploaded yet. Please upload a CSV file first.")
            return

        # -------- KPI CARDS --------
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Income", f"₹ {summary.get('income', 0):,.2f}")
        col2.metric("Expense", f"₹ {summary.get('expense', 0):,.2f}")
        col3.metric("Net Savings", f"₹ {summary.get('income', 0) - summary.get('expense', 0):,.2f}")
        col4.metric("Top Category", summary.get("top_category", "N/A"))

        st.divider()

        # -------- PIE CHART --------
        st.subheader("Expense Distribution")

        if "type" in df.columns and "category" in df.columns:
            category_data = df[df["type"] == "debit"].groupby("category")["amount"].sum()
            # Convert to absolute values (ensure positive for pie chart)
            category_data = category_data.abs()
            
            if not category_data.empty and (category_data > 0).any():
                fig1, ax1 = plt.subplots()
                ax1.pie(category_data, labels=category_data.index, autopct="%1.1f%%")
                st.pyplot(fig1)
            else:
                st.info("No expense data available for pie chart")
        else:
            st.error("Missing required columns: type, category")

        st.divider()

        # -------- BAR CHART --------
        st.subheader("Category Spending")

        if "type" in df.columns and "category" in df.columns:
            category_data = df[df["type"] == "debit"].groupby("category")["amount"].sum()
            # Convert to absolute values for consistent display
            category_data = category_data.abs()
            
            if not category_data.empty and (category_data > 0).any():
                fig2, ax2 = plt.subplots()
                category_data.plot(kind="bar", ax=ax2)
                ax2.set_title("Spending by Category")
                ax2.set_xlabel("Category")
                ax2.set_ylabel("Amount (₹)")
                st.pyplot(fig2)
            else:
                st.info("No expense data available for bar chart")
        else:
            st.error("Missing required columns: type, category")

        st.divider()

        # -------- WEEKLY TREND --------
        st.subheader("Weekly Expense Trend")

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            if "type" in df.columns:
                weekly = df[df["type"] == "debit"].groupby(pd.Grouper(key="date", freq="W"))["amount"].sum()
                # Convert to absolute values for consistent display
                weekly = weekly.abs()
                
                if not weekly.empty and (weekly > 0).any():
                    fig3, ax3 = plt.subplots()
                    weekly.plot(ax=ax3)
                    ax3.set_title("Weekly Expense Trend")
                    ax3.set_xlabel("Week")
                    ax3.set_ylabel("Amount (₹)")
                    st.pyplot(fig3)
                else:
                    st.info("No expense data available for trend chart")
            else:
                st.error("Missing required column: type")
        else:
            st.error("Missing required column: date")

        st.divider()

        # -------- TABLE --------
        st.subheader("Transactions")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")