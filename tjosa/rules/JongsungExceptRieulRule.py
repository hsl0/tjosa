from .JongsungRule import JongsungRule
from ..formatter import FallbackFormatter, format_fallback

__all__ = ["JongsungExceptRieulRule"]


class JongsungExceptRieulRule[T: str](JongsungRule[T]):
    """단어의 마지막 음절의 종성 존재 여부를 바탕으로 적절한 조사를 선택하는 변환 규칙

    단, 종성이 'ㄹ'일 경우에는 종성이 존재하지 않는 것으로 간주함."""

    def choose[F: str](
        self, word: str, *, fallback_formatter: FallbackFormatter[F] = format_fallback
    ):
        result = self._endswith_jongsung(word)

        if result is True:
            elc = ord(word[-1])
            if elc == 0x11AF or (0xAC00 <= elc <= 0xD7A3 and (elc - 0xAC00) % 28 == 8):
                result = False

        match result:
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
