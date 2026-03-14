"""josa_only 함수에 대한 테스트"""

from tjosa import josa_only


def test_english():
    assert josa_only("Test", "가") == "이(가)"
    assert josa_only("Testing", "이") == "(이)"


def test_custom_josa():
    custom_josa = ("있", "없")
    assert josa_only("받침", custom_josa) == "있"
    assert josa_only("없다", custom_josa) == "없"
