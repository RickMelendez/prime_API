from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar


T = TypeVar("T")
E = TypeVar("E", bound=Exception)


@dataclass
class Result(Generic[T]):
    value: Optional[T] = None
    error: Optional[E] = None

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def fail(cls, error: E) -> "Result[T]":
        return cls(error=error)