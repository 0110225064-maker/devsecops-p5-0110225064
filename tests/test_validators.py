import pytest

from app.validators import ValidationError, validate_expense


def test_valid_payload():
    out = validate_expense({"title": " Makan siang ", "amount": "25000", "category": "Makanan"})
    assert out == {"title": "Makan siang", "amount": 25000.0, "category": "makanan"}


@pytest.mark.parametrize("payload", [
    {"title": "", "amount": 1000},
    {"title": "x", "amount": "abc"},
    {"title": "x", "amount": -5},
    {"title": "x", "amount": 10, "category": "tidak-ada"},
    "bukan dict",
])
def test_invalid_payload(payload):
    with pytest.raises(ValidationError):
        validate_expense(payload)
