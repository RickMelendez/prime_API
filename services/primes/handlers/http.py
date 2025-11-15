from fastapi import APIRouter, Query
from services.primes.usecases.check_primality import CheckPrimalityUseCase


router = APIRouter(prefix="/primes", tags=["primes"])


@router.get("/check")
def check(n: int = Query(..., description="Number to check")):
    is_prime = CheckPrimalityUseCase().execute(n)
    return {"n": n, "is_prime": is_prime}