from fastapi import FastAPI


app = FastAPI(title="Primes Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "primes", "version": "0.1.0"}
from services.primes.handlers.http import router as primes_router

app.include_router(primes_router)
from libs.commons.middleware import add_observability

add_observability(app)
from fastapi import Response
from libs.commons.metrics import registry


@app.get("/metrics")
def metrics() -> Response:
    text = registry().render_prometheus()
    return Response(content=text, media_type="text/plain; version=0.0.4")