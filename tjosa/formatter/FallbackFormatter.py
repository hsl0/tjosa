"""FallbackFormatter 타입 모듈"""

from typing import Protocol
from abc import abstractmethod

__all__ = ["FallbackFormatter"]


class FallbackFormatter[T: str](Protocol):
    """조사 판별 불가 시 사용되는 폴백 포맷터 프로토콜"""

    @abstractmethod
    def __call__(self, *candidates: str) -> T: ...
