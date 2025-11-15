from fastapi.testclient import TestClient
from app.main import app


def test_response_includes_request_id_header():
    client = TestClient(app)
    resp = client.get("/primes/check", params={"n": 7})
    assert resp.status_code == 200
    assert "x-request-id" in resp.headers
    assert resp.headers["x-request-id"]