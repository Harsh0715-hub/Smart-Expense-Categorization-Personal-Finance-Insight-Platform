import requests

BASE_URL = "http://127.0.0.1:5000"

def test_upload():
    with open("sample_data/transactions.csv", "rb") as f:
        response = requests.post(f"{BASE_URL}/upload", files={"file": f})
    assert response.status_code == 200

def test_summary():
    response = requests.get(f"{BASE_URL}/summary")
    data = response.json()

    assert "income" in data
    assert "expense" in data
    assert "top_category" in data

def test_transactions():
    response = requests.get(f"{BASE_URL}/transactions")
    assert response.status_code == 200