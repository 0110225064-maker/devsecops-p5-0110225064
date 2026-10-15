import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app(":memory:").test_client()


def test_health(client):
    assert client.get("/health").json == {"status": "ok"}


def test_create_list_get_delete(client):
    r = client.post("/expenses", json={"title": "Kopi", "amount": 18000, "category": "makanan"})
    assert r.status_code == 201
    eid = r.json["id"]
    assert len(client.get("/expenses").json) == 1
    assert client.get("/expenses?category=transport").json == []
    assert client.get(f"/expenses/{eid}").json["title"] == "Kopi"
    assert client.delete(f"/expenses/{eid}").status_code == 204
    assert client.get(f"/expenses/{eid}").status_code == 404
    assert client.delete(f"/expenses/{eid}").status_code == 404


def test_create_invalid(client):
    assert client.post("/expenses", json={"title": "", "amount": 1}).status_code == 400


def test_summary(client):
    assert client.get("/summary").json["biggest"] is None
    client.post("/expenses", json={"title": "A", "amount": 100, "category": "belanja"})
    client.post("/expenses", json={"title": "B", "amount": 300, "category": "belanja"})
    data = client.get("/summary").json
    assert data["total"] == 400 and data["biggest"]["title"] == "B"
