import os
from fastapi import APIRouter, Depends, Query

from services.api_gateway.usecases.check_primality_proxy import CheckPrimalityProxyUseCase
from services.api_gateway.ports.prime_check import PrimeCheckPort
from services.api_gateway.adapters.http_primes_client import HttpPrimesClient


router = APIRouter(prefix="/primes", tags=["primes"], dependencies=[Depends(rate_limit)])


def get_prime_port() -> PrimeCheckPort:
    # Default runtime dependency
    return HttpPrimesClient(base_url=os.getenv("PRIMES_URL"))


@router.get("/check")
def check(n: int = Query(..., description="Number to check"), port: PrimeCheckPort = Depends(get_prime_port)):
    result = CheckPrimalityProxyUseCase(port).execute(n)
    return {"n": n, "is_prime": result}

from fastapi import HTTPException, Request
from libs.commons.ratelimit import FixedWindowRateLimiter


_RATE_LIMITER = FixedWindowRateLimiter(limit=5, window_seconds=1.0)


def get_rate_limiter() -> FixedWindowRateLimiter:
    return _RATE_LIMITER


def rate_limit(request: Request, limiter: FixedWindowRateLimiter = Depends(get_rate_limiter)) -> None:
    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")
    key = f"{client_ip}:{request.url.path}"
    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail={"error": {"type": "RateLimitExceeded", "message": "Too many requests"}})