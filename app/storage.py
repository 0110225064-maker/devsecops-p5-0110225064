"""Lapisan penyimpanan SQLite dengan query terparameter."""
import sqlite3
from typing import List, Optional

from app.models import Expense


class ExpenseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS expenses ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL)"
        )
        self._conn.commit()

    @staticmethod
    def _row_to_expense(row: sqlite3.Row) -> Expense:
        return Expense(id=row["id"], title=row["title"],
                       amount=row["amount"], category=row["category"])

    def add(self, expense: Expense) -> Expense:
        cur = self._conn.execute(
            "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
            (expense.title, expense.amount, expense.category),
        )
        self._conn.commit()
        expense.id = cur.lastrowid
        return expense

    def list_all(self, category: Optional[str] = None) -> List[Expense]:
        if category:
            rows = self._conn.execute(
                "SELECT * FROM expenses WHERE category = ? ORDER BY id", (category,)
            ).fetchall()
        else:
            rows = self._conn.execute("SELECT * FROM expenses ORDER BY id").fetchall()
        return [self._row_to_expense(r) for r in rows]

    def get(self, expense_id: int) -> Optional[Expense]:
        row = self._conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        return self._row_to_expense(row) if row else None

    def delete(self, expense_id: int) -> bool:
        cur = self._conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self._conn.commit()
        return cur.rowcount > 0
