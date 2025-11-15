from fastapi.testclient import TestClient
from app.main import app


def test_metrics_counter_increments_for_check_endpoint():
    client = TestClient(app)
    # Make two calls
    assert client.get("/primes/check", params={"n": 2}).status_code == 200
    assert client.get("/primes/check", params={"n": 3}).status_code == 200

    # Fetch metrics
    resp = client.get("/metrics")
    assert resp.status_code == 200
    body = resp.text
    # Expect a counter line with path="/primes/check" and status="200" and value 2
    want = 'http_requests_total{service="primes-service",method="GET",path="/primes/check",status="200"} 2'
    assert want in body