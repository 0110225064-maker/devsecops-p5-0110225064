# Pencatat Pengeluaran (Expense Tracker API)

## 1. Nama Aplikasi & Fungsi
**Expense Tracker API** adalah REST API sederhana untuk mencatat pengeluaran harian.
Pengguna dapat menambah, melihat (dengan filter kategori), dan menghapus pengeluaran,
serta melihat ringkasan total, total per kategori, dan pengeluaran terbesar.

## 2. Bahasa / Framework
- Python 3.11+
- Flask 3 (web framework), SQLite (penyimpanan, modul `sqlite3` bawaan Python)
- Pytest + pytest-cov (unit test & coverage), Bandit (SAST)

Struktur source code:

| File | Fungsi |
|---|---|
| `app/__init__.py` | Application factory |
| `app/models.py` | Model data `Expense` & daftar kategori |
| `app/validators.py` | Validasi input pengguna |
| `app/storage.py` | Repository SQLite (query terparameter) |
| `app/services.py` | Logika bisnis (total, ringkasan, anggaran) |
| `app/routes.py` | Endpoint REST |
| `run.py` | Entry point |
| `tests/` | 13 unit test |

## 3. Cara Menjalankan
```bash
git clone https://github.com/<username>/devsecops-p5-<nim>.git
cd devsecops-p5-<nim>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python run.py            # server berjalan di http://127.0.0.1:5000
pytest --cov=app         # menjalankan unit test
bandit -r app run.py     # menjalankan SAST secara lokal
```

Contoh pemakaian:
```bash
curl -X POST http://127.0.0.1:5000/expenses -H "Content-Type: application/json" \
     -d '{"title":"Makan siang","amount":25000,"category":"makanan"}'
curl http://127.0.0.1:5000/expenses
curl http://127.0.0.1:5000/summary
```

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/health` | Cek status |
| POST | `/expenses` | Tambah pengeluaran |
| GET | `/expenses?category=` | Daftar pengeluaran |
| GET/DELETE | `/expenses/<id>` | Detail / hapus |
| GET | `/summary` | Ringkasan |

## 4. Overview Pipeline CI/CD
Workflow: [`.github/workflows/devsecops.yml`](.github/workflows/devsecops.yml)

**Trigger:** `push` dan `pull_request` ke branch `main`.

```
build (ubuntu-latest) ──needs──▶ sast-scan (ubuntu-latest)
```

| Job | Isi | Quality Gate |
|---|---|---|
| `build` | Checkout, setup Python, install dependency, `pytest` + coverage | Gagal jika test gagal atau coverage < 70% |
| `sast-scan` | Bandit (laporan JSON sebagai artifact) | Gagal jika ada temuan severity **MEDIUM/HIGH** |
