"""josa_only 함수에 대한 테스트"""

from tjosa import josa_only
from tjosa.rules import JongsungRule

def test_english():
    '''영어 사용 테스트'''
    assert josa_only("Test", "가") == "이(가)"
    assert josa_only("Testing", "이") == "(이)"


def test_custom_josa():
    '''사용자 지정 조사 튜플 사용 테스트'''
    custom_rule = JongsungRule("있", "없")
    assert josa_only("받침", custom_rule) == "있"
    assert josa_only("없다", custom_rule) == "없"
