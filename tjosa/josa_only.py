"""josa_only 함수 모듈"""

from .mappings import josa_map, BuiltinJosa, ConversionMap
from .rules import ConversionRule
from .formatter import FallbackFormatter, format_fallback


def josa_only[C: str, K: str, F: str](
    cheon: str,
    josa: K | ConversionRule[C],
    *,
    fallback_formatter: FallbackFormatter[F] = format_fallback,
    conversion_rules: ConversionMap[K] = josa_map,
) -> str:
    """체언과 조사를 입력해서 체언에 맞는 조사를 반환합니다.

    '이' 조사는 생략 또는 '이'를 반환하므로, 이/가가 필요한 경우 '이' 대신에 '가'를 사용해 주세요.

    조사는 다음 중 하나를 선택하거나, ConversionRule 객체를 입력할 수 있습니다.

    사용 가능 조사:
        은, 는, 이, 가, 을, 를, 과, 와, 으로, 로, 아, 야

    Args:
        cheon (str): 체언
        josa (ConversionRule | BuiltinJosa): 조사

    Returns:
        str: 체언에 맞게 변환된 조사

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

        >>> josa_only('철수', '이는')
        '는'

        >>> josa_only('지민', '이는')
        '이는'
    """

    tail = ""  # 이어지는 글자
    rule: ConversionRule[C] | ConversionRule[BuiltinJosa]  # 조사 튜플

    if josa in conversion_rules:
        # 사전 정의된 유효한 조사를 선택한 경우
        rule = conversion_rules[josa]  # type: ignore
    elif isinstance(josa, str) and josa[0] in conversion_rules:
        # 사전 정의된 유효한 조사로 시작하는 경우
        rule = conversion_rules[josa[0]]  # type: ignore
        tail = josa[1:]
    elif isinstance(josa, ConversionRule):
        # 사용자 지정 조사 매핑을 입력한 경우
        rule = josa
    else:
        raise TypeError(f"{josa_only(str(josa), '는')} 유효한 조사가 아닙니다")

    return rule.choose(cheon, fallback_formatter=fallback_formatter) + tail
