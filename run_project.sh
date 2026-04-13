#!/bin/bash

# Smart Expense Categorization Platform - Unix/Linux/Mac Startup Script

echo ""
echo "========================================"
echo "Smart Expense Categorization Platform"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies if needed
echo "Installing/updating dependencies..."
python3 -m pip install flask streamlit requests pandas matplotlib --quiet

# Start Flask Backend in background
echo ""
echo "Starting Flask Backend on http://127.0.0.1:5000..."
python3 app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 3

# Start Streamlit Dashboard
echo "Starting Streamlit Dashboard on http://localhost:8501..."
echo ""
echo "NOTE: Press Ctrl+C to stop both services"
echo ""

python3 -m streamlit run streamlit_app.py

# Kill Flask when Streamlit is closed
kill $FLASK_PID 2>/dev/null
