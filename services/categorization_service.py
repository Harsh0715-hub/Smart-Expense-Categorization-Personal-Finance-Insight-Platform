# services/categorization_service.py

import pandas as pd

# Central keyword mapping
CATEGORY_KEYWORDS = {
    "Income": ["salary", "bonus", "interest", "credit"],
    "Rent": ["rent"],
    "Food": ["swiggy", "zomato", "dominos", "starbucks", "restaurant"],
    "Travel": ["uber", "ola", "trip", "cab", "bike"],
    "Shopping": ["amazon", "flipkart", "store", "order"],
    "Utilities": ["electricity", "water", "bill", "recharge"],
    "Entertainment": ["netflix", "spotify", "bookmyshow", "prime"],
    "Healthcare": ["apollo", "medplus", "pharmacy", "hospital"],
    "Insurance": ["insurance"],
    "Transfers": ["transfer", "upi"],
}


def categorize_transaction(description: str) -> str:
    """
    Assign category based on keyword matching
    """
    description = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Other"


def apply_categorization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add category column to dataframe
    """
    df["category"] = df["cleaned_description"].apply(categorize_transaction)
    return df