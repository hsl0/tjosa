"""기본 조사 데이터"""

from typing import Literal, cast
from .utils import create_josa_dict
from .types import Josa

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

# 기본 조사 매핑
default_josas: dict[DefinedJosa, Josa[DefinedJosa]] = cast(
    dict[DefinedJosa, Josa[DefinedJosa]],
    create_josa_dict(
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
    ),
)
