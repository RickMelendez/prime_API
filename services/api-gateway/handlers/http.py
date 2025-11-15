import os
from fastapi import APIRouter, Depends, Query

from services.api_gateway.usecases.check_primality_proxy import CheckPrimalityProxyUseCase
from services.api_gateway.ports.prime_check import PrimeCheckPort
from services.api_gateway.adapters.http_primes_client import HttpPrimesClient


router = APIRouter(prefix="/primes", tags=["primes"])


def get_prime_port() -> PrimeCheckPort:
    # Default runtime dependency
    return HttpPrimesClient(base_url=os.getenv("PRIMES_URL"))


@router.get("/check")
def check(n: int = Query(..., description="Number to check"), port: PrimeCheckPort = Depends(get_prime_port)):
    result = CheckPrimalityProxyUseCase(port).execute(n)
    return {"n": n, "is_prime": result}