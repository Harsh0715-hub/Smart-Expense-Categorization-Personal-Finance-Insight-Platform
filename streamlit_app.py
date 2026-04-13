import streamlit as st
import requests
from streamlit_pages.dashboard import show_dashboard
from streamlit_pages.reports import show_reports

API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Smart Expense Platform", layout="wide")

st.title("💰 Smart Expense Categorization Platform")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Upload", "Dashboard", "Reports"])

# ---------------- UPLOAD SCREEN ----------------
if menu == "Upload":
    st.header("📂 Upload Transactions CSV")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Uploaded Successfully! Rows Processed: {data['rows']}")
        else:
            st.error("Upload Failed")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    show_dashboard(API_BASE_URL)

# ---------------- REPORTS ----------------
elif menu == "Reports":
    show_reports(API_BASE_URL)