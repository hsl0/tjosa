"""josa 함수 모듈

Python 3.14 이상 필요
"""

from sys import version_info

if version_info.major < 3 or version_info.minor < 14:
    raise ImportError(
        f"t-string을 사용하는 josa() 함수는 Python 3.14 이상 버전이 필요합니다. 현재 Python 버전은 {version_info.major}.{version_info.minor} 입니다."
    )

from string.templatelib import Template
from typing import Sequence, Optional, cast
from .core import josa_core
from .types import Josa
from .josas import default_josas, DefinedJosa
from .utils import create_josa_dict


def josa[T: str, U: str](
    template: Template,
    *,
    custom_josas: Optional[Sequence[Josa[T, U]]] = None,
    unused_josas: Optional[Sequence[DefinedJosa]] = None,
) -> str:
    """템플릿 문자열에서 삽입되는 값에 맞게 조사를 변환합니다.

    Args:
        template (Template): 템플릿 문자열 (t-string)
        custom_josas (Sequence[Josa]): 사용자 지정 조사 튜플들
        unused_josas (Sequence[DefinedJosa]): 변환 대상에서 제외할 기본 조사들

    Returns:
        str: 조사를 변환한 문자열

    Examples:
        >>> food = '사과'
        >>> josa(t'{food}는 맛있다')
        '사과는 맛있다'

        >>> food = '파인애플'
        >>> josa(t'{food}는 맛있다')
        '파인애플은 맛있다'

        >>> building = '집'
        >>> josa(t'{building}은 크다')
        '집은 크다'

        >>> building = '학교'
        >>> josa(t'{building}은 크다')
        '학교는 크다'

        >>> animal = '고양이'
        >>> josa(t'{animal}이 잔다')
        '고양이가 잔다'

        >>> animal = '표범'
        >>> josa(t'{animal}이 잔다')
        '표범이 잔다'

        >>> drink = '물'
        >>> josa(t'{drink}를 마신다')
        '물을 마신다'

        >>> drink = '콜라'
        >>> josa(t'{drink}를 마신다')
        '콜라를 마신다'

        >>> tools = ('책', '펜')
        >>> josa(t'{tools[0]}과 {tools[1]}')
        '책과 펜'

        >>> tools = ('컴퓨터', '마우스')
        >>> josa(t'{tools[0]}과 {tools[1]}')
        '컴퓨터와 마우스'

        >>> destination = '학교'
        >>> josa(t'{destination}으로 간다')
        '학교로 간다'

        >>> destination = '집'
        >>> josa(t'{destination}으로 간다')
        '집으로 간다'

        >>> friend = '철수'
        >>> josa(t'{friend}야 안녕')
        '철수야 안녕'

        >>> friend = '지민'
        >>> josa(t'{friend}야 안녕')
        '지민아 안녕'

        >>> friend = '철수'
        >>> josa(t'{friend}이는 내 친구')
        '철수는 내 친구'

        >>> friend = '지민'
        >>> josa(t'{friend}이는 내 친구')
        '지민이는 내 친구'
    """

    josas = cast(
        dict[T | U | DefinedJosa, Josa[T, U] | Josa[DefinedJosa]],
        (
            default_josas
            if not custom_josas
            else default_josas | create_josa_dict(custom_josas)
        ),
    )

    if unused_josas:
        if josas is default_josas:
            josas = josas.copy()

        for jname in unused_josas:
            del josas[jname]

    fragments = [template.strings[0]]  # 완성된 문자열

    # e = 삽입된 어간
    # t = 어간 뒷부분
    for e, t in zip(template.values, template.strings[1:], strict=True):
        j = ""  # 인식된 조사

        if t[0:2] in josas:  # 두글자 조사 우선
            j = josas[cast(T | U | DefinedJosa, t[0:2])]
            t = t[2:]
        elif t[0:1] in josas:
            j = josas[cast(T | U | DefinedJosa, t[0])]
            t = t[1:]
        else:  # 조사가 아니면 그냥 연결
            fragments.append(e + t)
            continue

        jor = josa_core(e, j)  # 변환된 조사
        t = jor + t
        fragments.append(e + t)

    return "".join(fragments)
