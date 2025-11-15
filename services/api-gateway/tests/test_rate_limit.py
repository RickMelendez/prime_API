from fastapi.testclient import TestClient
from app.main import app
from services.api_gateway.handlers.http import get_rate_limiter
from libs.commons.ratelimit import FixedWindowRateLimiter


def test_rate_limit_exceeded_returns_429():
    limiter = FixedWindowRateLimiter(limit=2, window_seconds=10)
    app.dependency_overrides[get_rate_limiter] = lambda: limiter

    client = TestClient(app)
    headers = {"x-forwarded-for": "1.2.3.4"}

    assert client.get("/primes/check", params={"n": 2}, headers=headers).status_code == 200
    assert client.get("/primes/check", params={"n": 3}, headers=headers).status_code == 200
    resp = client.get("/primes/check", params={"n": 5}, headers=headers)
    assert resp.status_code == 429

    app.dependency_overrides.clear()