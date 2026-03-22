from typing import Iterator

from .ConversionRule import ConversionRule
from ..formatter import FallbackFormatter, format_fallback

__all__ = ["JongsungRule"]


class JongsungRule[T: str](ConversionRule[T]):
    """단어의 마지막 음절의 종성 존재 여부를 바탕으로 적절한 조사를 선택하는 변환 규칙"""

    # 마지막 음절에 종성이 있을 때
    with_jongsung: T
    # 마지막 음절에 종성이 없을 때
    without_jongsung: T

    def __init__(self, with_jongsung: T, without_jongsung: T):
        """단어의 마지막 음절의 종성 존재 여부를 바탕으로 적절한 조사를 선택하는 변환 규칙

        Args:
            with_jongsung (str): 마지막 음절에 종성이 있을 때 사용할 조사
            without_jongsung (str): 마지막 음절에 종성이 없을 때 사용할 조사
        """
        self.with_jongsung = with_jongsung
        self.without_jongsung = without_jongsung

    @staticmethod
    def _endswith_jongsung(word: str) -> bool | None:
        """단어가 종성으로 끝나는 지 여부를 반환

        Args:
            word (str): 단어

        Returns:
            bool | None:
                True: 단어의 마지막 음절에 종성이 있음
                False: 단어의 마지막 음절에 종성이 없음
                None: 판정 불가 (한글이 아님)
        """

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

    def __repr__(self):
        return format_fallback(*self.get_candidates())
