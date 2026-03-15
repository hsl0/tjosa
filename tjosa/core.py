"""공통 로직 모듈"""

from .types import Josa


def josa_core[T: str, U: str](eogan: str, josa_tuple: Josa[T, U]) -> T | U | str:
    """어간과 조사 튜플을 받아 어간에 맞는 조사를 선택합니다."""

    elc = ord(eogan[-1])  # 마지막 자모 코드

    if 0xAC00 <= elc <= 0xD7A3:  # NFC
        if (elc - 0xAC00) % 28 != 0:  # 받침 있음
            return josa_tuple[0]
        else:  # 받침 없음
            return josa_tuple[1]
    elif 0x11A8 <= elc <= 0x11C2:  # elc == NFD 종성 -> 받침 있음
        return josa_tuple[0]
    elif 0x1161 <= elc <= 0x1175:  # elc == NFD 중성 -> 받침 없음
        return josa_tuple[1]
    else:  # 판정 불가
        rspace = " " if josa_tuple[0][-1] == " " else ""
        if josa_tuple[1]:
            return f"{josa_tuple[0].strip()}({josa_tuple[1].strip()}){rspace}"
        else:
            return f"({josa_tuple[0].strip()}){rspace}"
