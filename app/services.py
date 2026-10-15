"""Logika bisnis: ringkasan dan statistik pengeluaran."""
from collections import defaultdict
from typing import Dict, List

from app.models import Expense


def total_amount(expenses: List[Expense]) -> float:
    return round(sum(e.amount for e in expenses), 2)


def summary_by_category(expenses: List[Expense]) -> Dict[str, float]:
    result: Dict[str, float] = defaultdict(float)
    for e in expenses:
        result[e.category] += e.amount
    return {k: round(v, 2) for k, v in sorted(result.items())}


def biggest_expense(expenses: List[Expense]):
    if not expenses:
        return None
    return max(expenses, key=lambda e: e.amount)


def budget_status(expenses: List[Expense], budget: float) -> dict:
    spent = total_amount(expenses)
    return {
        "budget": budget,
        "spent": spent,
        "remaining": round(budget - spent, 2),
        "over_budget": spent > budget,
    }
