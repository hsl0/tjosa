from typing import Literal, Iterable
from ..rules import JongsungRule, JongsungExceptRieulRule, ConversionRule
from .ConversionMap import ConversionMap

__all__ = ["josa_map", "josa_rules", "BuiltinJosa"]

type BuiltinJosa = Literal[
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
josa_rules: Iterable[ConversionRule[BuiltinJosa]] = [  # (받침 있음, 받침 없음)
    # 참조: 국립국어원 표준국어대사전 (CC BY-SA 2.0 KR)
    # 은 (4): [조사] 받침 있는 체언이나 부사어, 합성 동사의 선행 요소 따위의 뒤에 붙어
    # 는 (1): [조사] 받침 없는 체언이나 부사어, 연결 어미 ‘-아’, ‘-게’, ‘-지’, ‘-고’, 합성 동사의 선행 요소 따위의 뒤에 붙어
    JongsungRule[Literal["은", "는"]]("은", "는"),
    # 이 (25): [조사] 받침 있는 체언 뒤에 붙어
    # 가 (11): [조사] 받침 없는 체언 뒤에 붙어
    JongsungRule[Literal["이", "가"]]("이", "가"),
    JongsungRule[Literal["이 ", "가 "]]("이 ", "가 "),
    # 을 (2): [조사] 받침 있는 체언 뒤에 붙어
    # 를: [조사] 받침 없는 체언 뒤에 붙어
    JongsungRule[Literal["을", "를"]]("을", "를"),
    # 과 (12): [조사] (조건이 명시되지 않음)
    # 와 (3): [조사] (조건이 명시되지 않음)
    JongsungRule[Literal["과", "와"]]("과", "와"),
    # 으로: [조사] ‘ㄹ’을 제외한 받침 있는 체언 뒤에 붙어
    # 로 (6): [조사] 받침 없는 체언이나 ‘ㄹ’ 받침으로 끝나는 체언 뒤에 붙어
    JongsungExceptRieulRule[Literal["으로", "로"]]("으로", "로"),
    # 아 (9): [조사] 받침 있는 체언 뒤에 붙어
    # 야 (10): [조사] 받침 없는 체언 뒤에 붙어
    JongsungRule[Literal["아", "야"]]("아", "야"),
    # -이 (28): [접사] 받침 있는 사람의 이름 뒤에 붙어
    JongsungRule[Literal["이", ""]]("이", ""),  # type: ignore
]

josa_map = ConversionMap(josa_rules)
