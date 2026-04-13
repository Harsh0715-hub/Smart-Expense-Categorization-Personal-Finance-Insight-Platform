from database.db_config import get_connection


class TransactionRepository:
    """
    Handles all transaction table database operations.
    """

    @staticmethod
    def replace_transactions(df):
        """
        Clears old data and inserts latest uploaded transactions.
        Prevents duplicate rows during multiple uploads.
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Clear previous uploaded data for clean dashboard results
            cursor.execute("DELETE FROM transactions")

            insert_query = """
                INSERT INTO transactions (
                    date,
                    description,
                    cleaned_description,
                    amount,
                    type,
                    category
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """

            data_to_insert = [
                (
                    str(row["date"]),  # Ensure date is string format
                    row["description"],
                    row["cleaned_description"],
                    float(row["amount"]),  # Ensure amount is numeric
                    row["type"],
                    row["category"]
                )
                for _, row in df.iterrows()
            ]

            cursor.executemany(insert_query, data_to_insert)

            conn.commit()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def fetch_all_transactions():
        """
        Fetches all stored transactions.
        Used by transactions API and summary API.
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM transactions
                ORDER BY date ASC
            """)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            if conn:
                conn.close()