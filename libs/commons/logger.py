import logging
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or "app")
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger