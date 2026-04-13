from flask import Flask

from controllers.transaction_controller import transaction_bp
from database.db_config import init_db


def create_app():
    """
    Flask application factory.
    Keeps app modular and test-friendly.
    """
    app = Flask(__name__)

    # Initialize SQLite schema
    init_db()

    # Register all transaction routes
    app.register_blueprint(transaction_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)