from typing import Sequence
from .types import Josa


def create_josa_dict(josas: Sequence[Josa]) -> dict[str, Josa]:
    """조사 튜플의 모든 조사를 dict 형태로 매핑"""
    return {
        j: josa for josa in josas for j in josa if j
    }  # 튜플의 각 원소를 dict 키로, 튜플을 값으로 할당. 단, 빈 문자열은 키로 할당하지 않음
