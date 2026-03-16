from typing import Iterator

from .ConversionRule import ConversionRule
from ..formatter import FallbackFormatter, format_fallback

__all__ = ["JongsungRule"]


class JongsungRule[T: str](ConversionRule[T]):
    with_jongsung: T
    without_jongsung: T

    def __init__(self, with_jongsung: T, without_jongsung: T):
        self.with_jongsung = with_jongsung
        self.without_jongsung = without_jongsung

    @staticmethod
    def _endswith_jongsung(word: str) -> bool | None:
        elc = ord(word[-1])  # 마지막 자모 코드

        if 0xAC00 <= elc <= 0xD7A3:  # NFC
            return (elc - 0xAC00) % 28 != 0  # 받침 유무
        elif 0x11A8 <= elc <= 0x11C2:  # elc == NFD 종성 -> 받침 있음
            return True
        elif 0x1161 <= elc <= 0x1175:  # elc == NFD 중성 -> 받침 없음
            return False
        else:  # 판정 불가
            return None

    def choose[F: str](
        self, word: str, *, fallback_formatter: FallbackFormatter[F] = format_fallback
    ):
        """어간과 조사 튜플을 받아 어간에 맞는 조사를 선택합니다."""

        match self._endswith_jongsung(word):
            case True:
                return self.with_jongsung
            case False:
                return self.without_jongsung
            case None:
                return fallback_formatter(*self.get_candidates())
            case _ as result:
                raise TypeError(
                    f"{type(self).__name__}._endswith_jongsung 메소드의 결과가 잘못됨: {result}"
                )

    def get_candidates(self) -> Iterator[T]:
        return filter(None, (self.with_jongsung, self.without_jongsung))
