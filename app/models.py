"""Model data untuk aplikasi Pencatat Pengeluaran."""
from dataclasses import dataclass, asdict
from typing import Optional

CATEGORIES = ("makanan", "transport", "belanja", "tagihan", "hiburan", "lainnya")


@dataclass
class Expense:
    title: str
    amount: float
    category: str
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)
