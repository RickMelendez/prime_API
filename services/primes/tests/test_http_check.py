from fastapi.testclient import TestClient
from app.main import app


def test_check_prime_via_http():
    client = TestClient(app)
    resp = client.get("/primes/check", params={"n": 7})
    assert resp.status_code == 200
    body = resp.json()
    assert body == {"n": 7, "is_prime": True}


def test_check_negative_is_false():
    client = TestClient(app)
    resp = client.get("/primes/check", params={"n": -11})
    assert resp.status_code == 200
    assert resp.json()["is_prime"] is False


def test_missing_n_returns_422():
    client = TestClient(app)
    resp = client.get("/primes/check")
    assert resp.status_code == 422