from fastapi import FastAPI


app = FastAPI(title="Primes Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "primes", "version": "0.1.0"}
from services.primes.handlers.http import router as primes_router

app.include_router(primes_router)