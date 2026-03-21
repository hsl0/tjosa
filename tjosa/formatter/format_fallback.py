"""기본 FallbackFormatter 모듈"""

from typing import Literal

__all__ = ["format_fallback"]


def _get_rspace(candidate: str) -> Literal[" ", ""]:
    """띄어쓰기가 요구되는 후보의 경우, 띄어쓰기를 반환

    Args:
        candidate (str): 조사 후보

    Returns:
        str: 빈 문자열 또는 공백

    Examples:
        >>> _get_rspace('이')
        ''

        >>> _get_rspace('이 ')
        ' '
    """
    return " " if candidate.endswith(" ") else ""


def format_fallback(*candidates: str) -> str:
    """조사 두개를 괄호 밖과 괄호 안에 표시

    Args:
        *candidates (str): 조사 후보들

    Returns:
        str:
            후보가 한 개일 경우, 괄호 안에 표시
            후보가 두 개일 경우, 하나를 괄호 밖에, 다른 하나를 괄호 밖에 표시
            후보가 세 개 이상일 경우, 앞의 두 개만 표시

    Examples:
        >>> format_fallback('이')
        '(이)'

        >>> format_fallback('은', '는')
        '은(는)'

        >>> format_fallback('일', '이', '삼')
        '일(이)'
    """
    match candidates:
        case (candidate,):
            return f"({candidate.strip()}){_get_rspace(candidate)}"
        case (a, b, *_):
            return f"{a.strip()}({b.strip()}){_get_rspace(a)}"
        case _:
            raise TypeError("적어도 한 개 이상의 조사 후보가 필요합니다.")
