"""Endpoint REST API."""
from flask import Blueprint, current_app, jsonify, request

from app import services
from app.models import Expense
from app.validators import ValidationError, validate_expense

bp = Blueprint("expenses", __name__)


def _repo():
    return current_app.config["REPO"]


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/expenses")
def create_expense():
    try:
        data = validate_expense(request.get_json(silent=True))
    except ValidationError as exc:
        return jsonify(error=str(exc)), 400
    saved = _repo().add(Expense(**data))
    return jsonify(saved.to_dict()), 201


@bp.get("/expenses")
def list_expenses():
    items = _repo().list_all(request.args.get("category"))
    return jsonify([e.to_dict() for e in items])


@bp.get("/expenses/<int:expense_id>")
def get_expense(expense_id):
    item = _repo().get(expense_id)
    if item is None:
        return jsonify(error="Data tidak ditemukan"), 404
    return jsonify(item.to_dict())


@bp.delete("/expenses/<int:expense_id>")
def delete_expense(expense_id):
    if not _repo().delete(expense_id):
        return jsonify(error="Data tidak ditemukan"), 404
    return "", 204


@bp.get("/summary")
def summary():
    items = _repo().list_all()
    biggest = services.biggest_expense(items)
    return jsonify(
        total=services.total_amount(items),
        by_category=services.summary_by_category(items),
        biggest=biggest.to_dict() if biggest else None,
    )
