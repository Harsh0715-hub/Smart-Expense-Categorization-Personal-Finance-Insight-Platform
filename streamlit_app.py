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
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Uploaded Successfully! Rows Processed: {data['rows']}")
            else:
                error_detail = response.json().get("message", "Unknown error")
                st.error(f"Upload Failed: {error_detail}")
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    show_dashboard(API_BASE_URL)

# ---------------- REPORTS ----------------
elif menu == "Reports":
    show_reports(API_BASE_URL)