from fastapi.testclient import TestClient
from app.main import app
from services.api_gateway.handlers.http import get_prime_port


class FakePrimesClient:
    def is_prime(self, n: int) -> bool:
        return n in (2, 3, 5, 7, 11)


def test_gateway_metrics_counter_increments():
    # Override dependency to avoid network
    app.dependency_overrides[get_prime_port] = lambda: FakePrimesClient()
    client = TestClient(app)
    assert client.get("/primes/check", params={"n": 7}).status_code == 200
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert 'http_requests_total{service="api-gateway",method="GET",path="/primes/check",status="200"}' in resp.text
    app.dependency_overrides.clear()