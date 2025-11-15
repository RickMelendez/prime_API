from fastapi.testclient import TestClient
from app.main import app
from services.api_gateway.handlers.http import get_prime_port


class FakePrimesClient:
    def is_prime(self, n: int) -> bool:  # pragma: no cover - simple stub
        return n in (2, 3, 5, 7, 11)


def test_gateway_check_uses_port_override():
    app.dependency_overrides[get_prime_port] = lambda: FakePrimesClient()
    client = TestClient(app)

    resp = client.get("/primes/check", params={"n": 7})
    assert resp.status_code == 200
    assert resp.json() == {"n": 7, "is_prime": True}

    resp = client.get("/primes/check", params={"n": 8})
    assert resp.status_code == 200
    assert resp.json()["is_prime"] is False

    # Clean up override
    app.dependency_overrides.clear()


def test_missing_n_returns_422():
    client = TestClient(app)
    resp = client.get("/primes/check")
    assert resp.status_code == 422