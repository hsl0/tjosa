"""변환 규칙 매핑 모듈"""

from typing import Iterable
from ..rules import ConversionRule

__all__ = ["create_conversion_map", "ConversionMap"]

# 변환 규칙 매핑 타입
type ConversionMap[T: str] = dict[T, ConversionRule[T]]


def create_conversion_map[T: str](
    rules: Iterable[ConversionRule[T]],
) -> ConversionMap[T]:
    """변환 규칙 매핑 데이터 생성

    Args:
        rules (Iterable[ConversionRule[T]]): 변환 규칙들

    Returns:
        ConversionMap[T]: 변환 규칙 매핑 데이터
    """
    return {
        candidate: rule  # ConversionRule 객체의 각 후보를 dict 키로, 객체를 값으로 할당.
        for rule in rules
        for candidate in rule.get_candidates()
        if candidate  # 단, 빈 문자열인 후보는 키로 할당하지 않음
    }
