import pandas as pd
from flask import Blueprint, request, jsonify

from repositories.transaction_repository import TransactionRepository

# Member 2 ownership
from services.cleaning_service import DataCleaningService

# Member 3 ownership
from services.categorization_service import apply_categorization
from services.summary_service import generate_summary


transaction_bp = Blueprint("transaction_bp", __name__)


@transaction_bp.route("/upload", methods=["POST"])
def upload_transactions():
    """
    Upload CSV -> Clean -> Categorize -> Store
    """
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "CSV file is required"
            }), 400

        file = request.files["file"]

        df = pd.read_csv(file)

        # Member 2 layer
        cleaning_service = DataCleaningService()
        cleaned_df = cleaning_service.clean_data(df)

        # Member 3 layer
        categorized_df = apply_categorization(cleaned_df)

        # Member 1 DB layer
        TransactionRepository.replace_transactions(categorized_df)

        return jsonify({
            "status": "success",
            "rows": len(categorized_df)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@transaction_bp.route("/transactions", methods=["GET"])
def get_transactions():
    """
    Returns all categorized transactions for UI table.
    """
    try:
        transactions = TransactionRepository.fetch_all_transactions()
        return jsonify(transactions)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@transaction_bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Returns KPI summary for dashboard cards.
    """
    try:
        transactions = TransactionRepository.fetch_all_transactions()

        df = pd.DataFrame(transactions)

        if df.empty:
            return jsonify({
                "income": 0,
                "expense": 0,
                "top_category": "N/A"
            })

        summary = generate_summary(df)

        return jsonify({
            "income": summary["income"],
            "expense": summary["expense"],
            "top_category": summary["top_category"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500