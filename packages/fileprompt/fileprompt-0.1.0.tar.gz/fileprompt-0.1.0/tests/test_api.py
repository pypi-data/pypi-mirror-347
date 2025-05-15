from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tree_root():
    res = client.get("/api/tree")
    assert res.status_code == 200
    data = res.json()
    assert "path" in data


def test_copy_no_files():
    res = client.post("/api/copy", json={"root": ".", "selected": [], "instructions": "test"})
    assert res.status_code == 422
