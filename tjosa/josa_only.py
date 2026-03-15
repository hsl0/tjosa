from .josas import default_josas, DefinedJosa
from .types import Josa
from .core import josa_core


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

        >>> josa_only('철수', '이는')
        '는'

        >>> josa_only('지민', '이는')
        '이는'
    """

    t = ""  # 이어지는 글자

    if josa in default_josas:
        # 사전 정의된 유효한 조사를 선택한 경우
        j = default_josas[josa]
    elif isinstance(josa, str) and josa[0] in default_josas:
        # 사전 정의된 유효한 조사로 시작하는 경우
        j = default_josas[josa[0]]
        t = josa[1:]
    elif isinstance(josa, tuple) or isinstance(josa, str) and len(josa) == 2:
        # 사용자 지정 조사 매핑을 입력한 경우
        j = josa
    else:
        raise TypeError(f"{josa}(은)는 유효한 조사가 아닙니다")

    return josa_core(eogan, j) + t
