"""Application factory."""
import os

from flask import Flask

from app.storage import ExpenseRepository


def create_app(db_path: str = None) -> Flask:
    app = Flask(__name__)
    path = db_path or os.environ.get("EXPENSE_DB", ":memory:")
    app.config["REPO"] = ExpenseRepository(path)

    from app.routes import bp
    app.register_blueprint(bp)
    return app
