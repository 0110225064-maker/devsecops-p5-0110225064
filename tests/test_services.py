from app import services
from app.models import Expense


def sample():
    return [Expense("a", 10000, "makanan"), Expense("b", 50000, "transport"),
            Expense("c", 5000, "makanan")]


def test_total_and_summary():
    assert services.total_amount(sample()) == 65000
    assert services.summary_by_category(sample()) == {"makanan": 15000, "transport": 50000}


def test_biggest_and_empty():
    assert services.biggest_expense(sample()).title == "b"
    assert services.biggest_expense([]) is None


def test_budget_status():
    status = services.budget_status(sample(), 60000)
    assert status["over_budget"] is True
    assert status["remaining"] == -5000
