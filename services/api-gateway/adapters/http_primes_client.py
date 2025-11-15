import os
import httpx

from services.api_gateway.ports.prime_check import PrimeCheckPort


class HttpPrimesClient(PrimeCheckPort):
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("PRIMES_URL", "http://localhost:8001")

    def is_prime(self, n: int) -> bool:
        url = f"{self.base_url}/primes/check"
        resp = httpx.get(url, params={"n": n}, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        return bool(data.get("is_prime"))