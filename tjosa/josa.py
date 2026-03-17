"""josa 함수 모듈

Python 3.14 이상 필요
"""

from sys import version_info

if version_info.major != 3 or version_info.minor < 14:
    raise ImportError(
        f"t-string을 사용하는 josa() 함수는 Python 3.14 이상 버전이 필요합니다. \
            현재 Python 버전은 {version_info.major}.{version_info.minor} 입니다."
    )

from string.templatelib import Template
from .rules import ConversionRule
from .formatter import FallbackFormatter, format_fallback
from .mappings import ConversionMap, josa_map


def josa[T: str, F: str](
    template: Template,
    *,
    conversion_rules: ConversionMap[T] = josa_map,
    fallback_formatter: FallbackFormatter[F] = format_fallback,
) -> str:
    """템플릿 문자열에서 삽입되는 값에 맞게 조사를 변환합니다.

    Args:
        template (Template): 템플릿 문자열 (t-string)
        conversion_rules (dict[T, ConversionRule[T]]): 사용자 지정 변환 규칙
        fallback_formatter (FallbackFormatter[U]): 판정 불가 시 폴백 포맷터 함수

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

        >>> tools = ('책', '깃펜')
        >>> josa(t'{tools[0]}과 {tools[1]}')
        '책과 깃펜'

        >>> tools = ('컴퓨터', '마우스')
        >>> josa(t'{tools[0]}과 {tools[1]}')
        '컴퓨터와 마우스'

        >>> horse = '제주'
        >>> human = '서울'
        >>> josa(t'말은 {horse}로, 사람은 {human}으로')
        '말은 제주로, 사람은 서울로'

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

    fragments = [template.strings[0]]  # 완성된 문자열

    # cheon = 삽입된 체언
    # tail = 체언 뒷부분
    for cheon, tail in zip(template.values, template.strings[1:], strict=True):
        key: T
        rule: ConversionRule[T]  # 인식된 조사

        if tail[0:2] in conversion_rules:  # 두글자 조사 우선
            key = tail[0:2]  # type: ignore
            rule = conversion_rules[key]
            tail = tail[2:]
        elif tail[0:1] in conversion_rules:
            key = tail[0]  # type: ignore
            rule = conversion_rules[key]
            tail = tail[1:]
        else:  # 조사가 아니면 그냥 연결
            fragments.append(cheon + tail)
            continue

        normalized_josa = rule.choose(
            cheon, fallback_formatter=fallback_formatter
        )  # 변환된 조사
        tail = normalized_josa + tail
        fragments.append(cheon + tail)

    return "".join(fragments)
