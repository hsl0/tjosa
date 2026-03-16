from typing import Literal

__all__ = ["format_fallback"]


def _get_rspace(candidate: str) -> Literal[" ", ""]:
    return " " if candidate.endswith(" ") else ""


def format_fallback(*candidates: str) -> str:
    match candidates:
        case (candidate,):
            return f"({candidate.strip()}){_get_rspace(candidate)}"
        case (a, b, *_):
            return f"{a.strip()}({b.strip()}){_get_rspace(a)}"
        case _:
            raise TypeError("적어도 한 개 이상의 조사 후보가 필요합니다.")
