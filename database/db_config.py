import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expense_data.db"


def get_connection():
    """
    Returns SQLite connection with row dictionary support.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes transactions table as per schema freeze.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            cleaned_description TEXT,
            amount REAL,
            type TEXT,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()