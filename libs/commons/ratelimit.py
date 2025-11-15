import time
from collections import deque, defaultdict
from typing import Deque, Dict


class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float = 1.0):
        self.limit = int(limit)
        self.window = float(window_seconds)
        self._buckets: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        window_start = now - self.window
        dq = self._buckets[key]
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= self.limit:
            return False
        dq.append(now)
        return True

    def reset(self) -> None:
        self._buckets.clear()