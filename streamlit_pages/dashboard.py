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
            try:
                # Convert amount to numeric
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
                
                # Get debit transactions and sum by category
                debit_df = df[df["type"] == "debit"].copy()
                debit_df["amount"] = debit_df["amount"].abs()
                
                category_data = debit_df.groupby("category")["amount"].sum()
                
                # Filter out zero and NaN values
                category_data = category_data[category_data > 0]
                
                if not category_data.empty:
                    fig1, ax1 = plt.subplots(figsize=(8, 6))
                    colors = plt.cm.Set3(range(len(category_data)))
                    ax1.pie(category_data, labels=category_data.index, autopct="%1.1f%%", colors=colors)
                    ax1.set_title("Expense Distribution by Category")
                    st.pyplot(fig1)
                else:
                    st.info("No expense data available for pie chart")
            except Exception as e:
                st.warning(f"Could not generate pie chart: {str(e)}")
        else:
            st.error("Missing required columns: type, category")

        st.divider()

        # -------- BAR CHART --------
        st.subheader("Category Spending")

        if "type" in df.columns and "category" in df.columns:
            try:
                # Convert amount to numeric
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
                
                # Get debit transactions and sum by category
                debit_df = df[df["type"] == "debit"].copy()
                debit_df["amount"] = debit_df["amount"].abs()
                
                category_data = debit_df.groupby("category")["amount"].sum()
                
                # Filter out zero and NaN values
                category_data = category_data[category_data > 0]
                
                if not category_data.empty:
                    fig2, ax2 = plt.subplots(figsize=(10, 6))
                    category_data.sort_values(ascending=False).plot(kind="bar", ax=ax2, color=plt.cm.Set2(range(len(category_data))))
                    ax2.set_title("Category Spending", fontsize=14, fontweight='bold')
                    ax2.set_xlabel("Category", fontsize=12)
                    ax2.set_ylabel("Amount (₹)", fontsize=12)
                    ax2.tick_params(axis='x', rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig2)
                else:
                    st.info("No expense data available for bar chart")
            except Exception as e:
                st.warning(f"Could not generate bar chart: {str(e)}")
        else:
            st.error("Missing required columns: type, category")

        st.divider()

        # -------- WEEKLY TREND --------
        st.subheader("Weekly Expense Trend")

        if "date" in df.columns:
            try:
                # Ensure date and amount are in correct format
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
                
                if "type" in df.columns:
                    # Get debit transactions and convert to absolute values
                    debit_df = df[df["type"] == "debit"].copy()
                    debit_df["amount"] = debit_df["amount"].abs()
                    
                    weekly = debit_df.groupby(pd.Grouper(key="date", freq="W"))["amount"].sum()
                    
                    # Filter out zero values
                    weekly = weekly[weekly > 0]
                    
                    if not weekly.empty:
                        fig3, ax3 = plt.subplots(figsize=(12, 6))
                        weekly.plot(ax=ax3, marker='o', color='#2E86AB', linewidth=2)
                        ax3.set_title("Weekly Expense Trend", fontsize=14, fontweight='bold')
                        ax3.set_xlabel("Week", fontsize=12)
                        ax3.set_ylabel("Amount (₹)", fontsize=12)
                        ax3.grid(True, alpha=0.3)
                        plt.tight_layout()
                        st.pyplot(fig3)
                    else:
                        st.info("No expense data available for trend chart")
                else:
                    st.error("Missing required column: type")
            except Exception as e:
                st.warning(f"Could not generate trend chart: {str(e)}")
        else:
            st.error("Missing required column: date")

        st.divider()

        # -------- TABLE --------
        st.subheader("Transactions")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")