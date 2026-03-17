"""기본 조사 데이터"""

from typing import Iterable
from ..rules import ConversionRule

__all__ = ["ConversionMap"]


class ConversionMap[T: str](dict[T, ConversionRule[T]]):
    def __init__(self, rules: Iterable[ConversionRule[T]]):
        super().__init__(
            {
                candidate: rule  # ConversionRule 객체의 각 후보를 dict 키로, 객체를 값으로 할당.
                for rule in rules
                for candidate in rule.get_candidates()
                if candidate  # 단, 빈 문자열인 후보는 키로 할당하지 않음
            }
        )
