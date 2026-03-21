"""tjosa.mappings 모듈 테스트"""

from unittest.mock import MagicMock
from tjosa.mappings import create_conversion_map


def create_conversion_rule_mock(*candidates: str):
    """ConversionRule Mock 객체 생성

    Args:
        *candidates (str): 가능한 변환 후보
    """
    mock = MagicMock()
    mock.get_candidates.return_value = candidates
    return mock


def test_create_conversion_map():
    """create_conversion_map 테스트"""
    eun_neun = create_conversion_rule_mock("은", "는")
    e = create_conversion_rule_mock("이", "")
    assert create_conversion_map([eun_neun, e]) == {"은": eun_neun, "는": eun_neun, "이": e}
