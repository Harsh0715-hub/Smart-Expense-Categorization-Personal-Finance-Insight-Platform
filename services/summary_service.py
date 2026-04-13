# services/summary_service.py

import pandas as pd


def generate_summary(df: pd.DataFrame) -> dict:
    """
    Generate financial summary
    """
    # Ensure numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Income & Expense
    income = df[df["type"] == "credit"]["amount"].sum()
    expense = df[df["type"] == "debit"]["amount"].sum()

    # Category totals (only expenses for charts)
    category_totals = (
        df[df["type"] == "debit"]
        .groupby("category")["amount"]
        .sum()
        .to_dict()
    )

    # Top spending category
    top_category = max(category_totals, key=category_totals.get) if category_totals else None

    return {
        "income": float(income),
        "expense": float(abs(expense)),
        "category_totals": category_totals,
        "top_category": top_category,
    }