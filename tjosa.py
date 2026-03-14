"""한국어 조사를 어간에 맞게 자동으로 맞춰주는 라이브러리입니다.
t-string을 통해 삽입한 값의 조사를 자동으로 인식해 변환하는 기능을 지원합니다.
"""

from string import Template
import unicodedata
from typing import Literal, Sequence

# export 대상 함수 목록
__all__ = ["josa", "josa_only"]

Josa = tuple[str, str]


def create_josa_dict(josas: Sequence[Josa]) -> dict[str, Josa]:
    """조사 튜플의 모든 조사를 dict 형태로 매핑"""
    return {
        j: josa for josa in josas for j in josa if j
    }  # 튜플의 각 원소를 dict 키로, 튜플을 값으로 할당. 단, 빈 문자열은 키로 할당하지 않음


# 기본 조사 매핑
DefinedJosa = Literal[
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "과",
    "와",
    "으로",
    "로",
    "아",
    "야",
    "이 ",
    "가 ",
]
defaultJosas: dict[DefinedJosa, Josa | str] = create_josa_dict(
    [  # (받침 있음, 받침 없음)
        ("은", "는"),
        ("이", "가"),
        ("이 ", "가 "),
        ("을", "를"),
        ("과", "와"),
        ("으로", "로"),
        ("아", "야"),
        ("이", ""),
    ]
)


def josa(
    template: Template,
    *,
    custom_josas: Sequence[Josa] = (),
    unused_josas: Sequence[DefinedJosa] = (),
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

    josas = defaultJosas | create_josa_dict(custom_josas)

    for jname in unused_josas:
        del josas[jname]

    composed = template.strings[0]  # 완성된 문자열

    # e = 삽입된 어간
    # t = 어간 뒷부분
    for e, t in zip(template.values, template.strings[1:], strict=True):
        j = ""  # 인식된 조사

        if t[0:2] in josas:  # 두글자 조사 우선
            j = josas[t[0:2]]
            t = t[2:]
        elif t[0:1] in josas:
            j = josas[t[0]]
            t = t[1:]
        else:  # 조사가 아니면 그냥 연결
            composed += e + t
            continue

        jor = josa_only(e, j)  # 변환된 조사
        t = jor + t
        composed += e + t

    return composed


def josa_only(eogan: str, josa: DefinedJosa | Josa) -> str:
    """어간과 조사를 입력해서 어간에 맞는 조사를 반환합니다.

    '이' 조사는 생략 또는 '이'를 반환하므로, 이/가가 필요한 경우 '이' 대신에 '가'를 사용해 주세요.

    조사는 다음 중 하나를 선택하거나, (받침 있음, 받침 없음)을 매핑한 사용자 지정 조사 튜플을 입력할 수 있습니다.

    사용 가능 조사:
        은, 는, 이, 가, 을, 를, 과, 와, 으로, 로, 아, 야

    Args:
        eogan (str): 어간
        josa (Josa | DefinedJosa): 조사

    Returns:
        str: 어간에 맞게 변환된 조사

    Raises:
        TypeError: josa에 유효한 조사가 아닌 다른 문자열을 입력했을 때 발생합니다.

    Examples:
        >>> josa_only('사과', '는')
        '는'

        >>> josa_only('파인애플', '는')
        '은'

        >>> josa_only('집', '은')
        '은'

        >>> josa_only('학교', '은')
        '는'

        >>> josa_only('고양이', '가')
        '가'

        >>> josa_only('표범', '가')
        '이'

        >>> josa_only('물', '를')
        '을'

        >>> josa_only('콜라', '를')
        '를'

        >>> josa_only('책', '과')
        '과'

        >>> josa_only('컴퓨터', '과')
        '와'

        >>> josa_only('학교', '으로')
        '로'

        >>> josa_only('집', '으로')
        '으로'

        >>> josa_only('철수', '야')
        '야'

        >>> josa_only('지민', '야')
        '아'

        >>> josa_only('철수', '이')
        ''

        >>> josa_only('지민', '이')
        '이'
    """

    if josa in defaultJosas:
        # 사전 정의된 유효한 조사를 선택한 경우
        j = defaultJosas[josa]
    elif isinstance(josa, tuple) or isinstance(josa, str) and len(josa) == 2:
        # 사용자 지정 조사 매핑을 입력한 경우
        j = josa
    else:
        raise TypeError(f"{josa}(은)는 유효한 조사가 아닙니다")

    ed = unicodedata.normalize("NFD", eogan[-1])  # 초성, 중성, 종성 분리
    edlc = ord(ed[-1])  # 마지막 자모 코드

    if 0x11A8 <= edlc <= 0x11C2:  # edlc == 종성 -> 받침 있음
        return j[0]
    elif 0x1161 <= edlc <= 0x1175:  # edlc == 중성 -> 받침 없음
        return j[1]
    else:  # 판정 불가
        rspace = " " if j[0][-1] == " " else ""
        if j[1]:
            return f"{j[0].strip()}({j[1].strip()}){rspace}"
        else:
            return f"({j[0].strip()}){rspace}"
