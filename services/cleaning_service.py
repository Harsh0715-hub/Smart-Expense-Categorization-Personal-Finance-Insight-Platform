import pandas as pd

from utils.csv_validator import CSVValidator


class DataCleaningService:

    def __init__(self):

        self.validator = CSVValidator()

    # Step 1 — Validate CSV
    def validate_data(self, df):

        self.validator.validate_columns(df)

        return df

    # Step 2 — Handle Null Values
    def handle_nulls(self, df):

        df["description"] = df["description"].fillna("Unknown")

        df["amount"] = df["amount"].fillna(0)

        df["date"] = df["date"].ffill()
        
        # Convert amount to numeric, handling any non-numeric values
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        return df

    # Step 3 — Remove Duplicates
    def remove_duplicates(self, df):

        df = df.drop_duplicates()

        return df

    # Step 4 — Normalize Description
    def normalize_description(self, df):

        df["cleaned_description"] = (
            df["description"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        return df

    # Step 5 — Clean Date
    def clean_date(self, df):

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )
        
        # Convert to ISO format string for SQLite compatibility
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        return df

    # Final Pipeline
    def clean_data(self, df):

        df = self.validate_data(df)

        df = self.handle_nulls(df)

        df = self.remove_duplicates(df)

        df = self.normalize_description(df)

        df = self.clean_date(df)

        return df
    