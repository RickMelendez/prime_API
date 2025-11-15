from typing import Protocol


class PrimeCheckPort(Protocol):
    def is_prime(self, n: int) -> bool:  # pragma: no cover - interface only
        ...