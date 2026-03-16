"""공통 로직 모듈"""

from typing import Protocol, Iterable, runtime_checkable
from abc import abstractmethod

from ..formatter import FallbackFormatter

__all__ = ["ConversionRule"]


@runtime_checkable
class ConversionRule[T: str](Protocol):
    @abstractmethod
    def choose[F: str](
        self, word: str, *, fallback_formatter: FallbackFormatter[F]
    ) -> T | F: ...

    @abstractmethod
    def get_candidates(self) -> Iterable[T]: ...
