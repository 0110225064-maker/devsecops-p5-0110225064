"""Validasi input pengguna sebelum disimpan."""
from app.models import CATEGORIES


class ValidationError(ValueError):
    """Dilempar ketika input tidak valid."""


def validate_expense(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValidationError("Payload harus berupa objek JSON")

    title = str(payload.get("title", "")).strip()
    if not title or len(title) > 100:
        raise ValidationError("Judul wajib diisi (maksimal 100 karakter)")

    try:
        amount = float(payload.get("amount"))
    except (TypeError, ValueError):
        raise ValidationError("Jumlah harus berupa angka")
    if amount <= 0:
        raise ValidationError("Jumlah harus lebih besar dari 0")

    category = str(payload.get("category", "lainnya")).lower()
    if category not in CATEGORIES:
        raise ValidationError("Kategori tidak dikenal: " + category)

    return {"title": title, "amount": amount, "category": category}
