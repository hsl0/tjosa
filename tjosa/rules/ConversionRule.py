"""ConversionRule 프로토콜 모듈"""

from typing import Protocol, Iterable, runtime_checkable
from abc import abstractmethod

from ..formatter import FallbackFormatter

__all__ = ["ConversionRule"]


@runtime_checkable
class ConversionRule[T: str](Protocol):
    """변환 규칙 클래스 프로토콜"""

    @abstractmethod
    def choose[F: str](self, word: str, *, fallback_formatter: FallbackFormatter[F]) -> T | F:
        """체언에 맞는 조사를 선택합니다.

        Args:
            word (str): 조사를 부착할 체언
            fallback_formatter (FallbackFormatter[F]): 판정 불가 시 대신 반환할 조사의 포맷터 함수

        Returns:
            str: 체언에 적절한 조사 또는 판정 불가 시 폴백 문자열
        """

    @abstractmethod
    def get_candidates(self) -> Iterable[T]:
        """가능한 조사 후보들을 반환합니다.

        Returns:
            Iterable[str]: 조사 후보들
        """
