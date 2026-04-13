# Smart Expense Categorization Platform - Complete Setup & Run Guide

## 📋 Project Overview

This project consists of:
- **Backend**: Flask API server (Port 5000) - Handles data processing, cleaning, categorization
- **Frontend**: Streamlit Dashboard (Port 8501) - Web UI for uploading, viewing analytics & reports
- **Database**: SQLite (expense_data.db) - Local data storage

---

## 🔧 Prerequisites

Ensure Python 3.8+ is installed on your system:
```bash
python --version
```

---

## 📦 Installation (One-Time Setup)

### Step 1: Navigate to the project directory
```bash
cd "path/to/Smart-Expense-Categorization-Personal-Finance-Insight-Platform"
```

### Step 2: Install Required Dependencies
```bash
pip install flask streamlit requests pandas matplotlib
```

Or if you have a requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### **Option 1: Run in Two Separate Terminal Windows (Recommended)**

#### Terminal 1 - Start Flask Backend
```bash
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

#### Terminal 2 - Start Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

### **Option 2: Use Batch Script (Windows)**

Create a file named `run_project.bat` in the project root:

```batch
@echo off
START python app.py
TIMEOUT /T 2
START streamlit run streamlit_app.py
```

Then double-click `run_project.bat` to run both services.

---

### **Option 3: Use Shell Script (Mac/Linux)**

Create a file named `run_project.sh` in the project root:

```bash
#!/bin/bash
python app.py &
sleep 2
streamlit run streamlit_app.py
```

Give it execute permissions and run:
```bash
chmod +x run_project.sh
./run_project.sh
```

---

## 🌐 Access the Application

Once both services are running:

1. **Open Dashboard**: http://localhost:8501
2. **Backend API**: http://127.0.0.1:5000

---

## 📝 Using the Platform

### Step 1: Validate Your Data (NEW!)
- Go to **Validate** tab in the dashboard
- Upload your CSV file to validate before processing
- Review validation results:
  - ✅ Column presence and format checks
  - ⚠️ Warnings for missing values, duplicates, invalid formats
  - ❌ Errors that must be fixed
  - 📊 Data summary statistics
  - 💰 Financial overview
  - 👀 Data preview with detailed statistics
- Fix any errors and re-validate until it passes
- Click "Proceed to Upload" when validation passes

### Step 2: Upload Transactions CSV
- Go to **Upload** tab in the dashboard
- Upload your CSV file with columns: `date`, `description`, `amount`, `type`
- Click "Upload" to process

**Example CSV format:**
```
date,description,amount,type
2026-01-01,SALARY CREDIT ACME CORP,85000,credit
2026-01-01,RENT PAYMENT APT 4B,-25000,debit
2026-01-02,SWIGGY ORDER,620,debit
```

### Step 3: View Dashboard
- Go to **Dashboard** tab
- See KPI cards (Income, Expense, Savings, Top Category)
- View charts: Expense Distribution, Category Spending, Weekly Trends
- Check transaction table

### Step 4: Generate Reports
- Go to **Reports** tab
- Select a category from dropdown
- View detailed spending report for that category

---

## 🛠️ Troubleshooting

### Port Already In Use
If port 5000 or 8501 is already in use:

**Flask (Port 5000):**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows, replace PID)
taskkill /PID <PID> /F
```

**Streamlit (Port 8501):**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Module Not Found Error
If you get "No module named 'flask'" or similar:
```bash
pip install --upgrade flask streamlit requests pandas matplotlib
```

### Database Issues
If you encounter database errors, delete the `expense_data.db` file:
```bash
rm expense_data.db
```
The database will be recreated automatically on next run.

### Backend Not Responding
Ensure Flask is running on correct URL in streamlit_app.py:
```python
API_BASE_URL = "http://127.0.0.1:5000"
```

---

## 📊 Project Structure

```
Smart-Expense-Categorization-Platform/
├── app.py                      # Flask app entry point
├── streamlit_app.py            # Streamlit dashboard entry point
├── controllers/
│   └── transaction_controller.py  # API routes
├── services/
│   ├── cleaning_service.py        # Data cleaning logic
│   ├── categorization_service.py  # Category assignment logic
│   └── summary_service.py         # Summary generation
├── repositories/
│   └── transaction_repository.py  # Database operations
├── database/
│   └── db_config.py               # Database configuration
├── streamlit_pages/
│   ├── validation.py              # Data validation page (NEW!)
│   ├── dashboard.py               # Dashboard UI
│   └── reports.py                 # Reports UI
├── utils/
│   ├── csv_validator.py           # CSV validation
│   └── error_tracker.py           # Error tracking
└── sample_data/
    └── transactions.csv           # Sample data
```

---

## 🔄 Data Flow

```
CSV Upload (Streamlit UI)
         ↓
    Flask API /upload
         ↓
  DataCleaningService (Clean & Validate)
         ↓
  CategorizationService (Assign Categories)
         ↓
  TransactionRepository (Store in SQLite)
         ↓
  Flask API /transactions & /summary
         ↓
  Streamlit Dashboard & Reports (Display)
```

---

## 📱 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload and process CSV |
| `/transactions` | GET | Fetch all transactions |
| `/summary` | GET | Get financial summary (income, expense, top category) |

---

## ✨ Data Validation Features

The **Validate** tab provides comprehensive data quality checks:

### Validation Checks:
- **Column Validation**: Ensures all required columns exist (`date`, `description`, `amount`, `type`)
- **Date Format Validation**: Checks if dates can be parsed correctly
- **Amount Format Validation**: Ensures amounts are numeric values
- **Transaction Type Validation**: Verifies only "credit" or "debit" values
- **Missing Values Detection**: Identifies null/missing data
- **Duplicate Detection**: Finds and reports duplicate rows
- **Amount Logic Validation**: 
  - Warns about zero amounts
  - Detects unusual patterns (e.g., negative credits, positive debits)

### Validation Output:
- ✅ **Success Messages**: Data quality confirmed
- ⚠️ **Warnings**: Issues that may affect analysis but won't block upload
- ❌ **Errors**: Critical issues that must be fixed
- 📊 **Data Summary**: Row counts, transaction types, financial totals
- 👀 **Data Preview**: Sample of the data with statistics
- 📈 **Column Statistics**: Data types, missing values, amount ranges

---

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install flask streamlit requests pandas matplotlib`)
- [ ] Sample data available at `sample_data/transactions.csv`
- [ ] Terminal 1: `python app.py` (Flask running on 5000)
- [ ] Terminal 2: `streamlit run streamlit_app.py` (Streamlit running on 8501)
- [ ] Open http://localhost:8501 in browser
- [ ] Go to **Validate** tab and upload CSV to validate data quality
- [ ] Fix any validation errors if needed
- [ ] Go to **Upload** tab and upload the validated CSV
- [ ] View analytics in **Dashboard** tab
- [ ] Check reports in **Reports** tab

---

## 📞 Support

If you encounter issues:
1. Check terminal output for error messages
2. Ensure both services are running in separate terminals
3. Verify dependencies are installed correctly
4. Check that ports 5000 and 8501 are available
5. Review error messages and troubleshooting section above

Happy expense tracking! 💰📊
