@echo off
REM Smart Expense Categorization Platform - Windows Startup Script

echo.
echo ========================================
echo Smart Expense Categorization Platform
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing/updating dependencies...
python -m pip install flask streamlit requests pandas matplotlib --quiet

REM Start Flask Backend in separate window
echo.
echo Starting Flask Backend on http://127.0.0.1:5000...
START "Flask Backend" cmd /k python app.py

REM Wait for Flask to start
timeout /t 3 /nobreak

REM Start Streamlit Dashboard
echo Starting Streamlit Dashboard on http://localhost:8501...
echo.
echo NOTE: Press Ctrl+C in this window to stop both services
echo.

streamlit run streamlit_app.py

pause
