import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from libs.commons.logger import get_logger


def add_observability(app: FastAPI) -> None:
    logger = get_logger("http")

    @app.middleware("http")
    async def request_logger(request: Request, call_next: Callable):  # type: ignore[override]
        start = time.perf_counter()
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        try:
            response = await call_next(request)
        except ValueError as exc:
            # Convert validation errors to 400 with structured body
            response = JSONResponse(
                status_code=400,
                content={"error": {"type": "ValidationError", "message": str(exc)}},
            )
        except Exception as exc:  # pragma: no cover - safety net
            response = JSONResponse(
                status_code=500,
                content={"error": {"type": "InternalError", "message": "unexpected error"}},
            )
            logger.exception("Unhandled exception", extra={"request_id": request_id})
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["x-request-id"] = request_id
        logger.info(
            "request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response