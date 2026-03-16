from typing import Protocol
from abc import abstractmethod

__all__ = ["FallbackFormatter"]


class FallbackFormatter[T: str](Protocol):
    @abstractmethod
    def __call__(self, *candidates: str) -> T: ...
