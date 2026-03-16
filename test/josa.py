'''josa 함수에 대한 테스트'''

from tjosa import josa
from tjosa.mappings import create_conversion_map
from tjosa.mappings.josa import josa_rules
from tjosa.rules import JongsungRule


def test_english():
    '''영어 사용 테스트'''
    assert josa(t'{"Test"}이 진행 중입니다.') == 'Test이(가) 진행 중입니다.'
    assert josa(t'현재 상태는 {"Testing"}이다.') == '현재 상태는 Testing(이)다.'


def test_custom_josas():
    '''사용자 지정 조사 사용 테스트'''
    conversion_rules = create_conversion_map([*josa_rules, JongsungRule('있', '없')])
    assert josa(t'{"받침"}있음', conversion_rules=conversion_rules) == '받침있음'
    assert josa(t'{"오류"}있음', conversion_rules=conversion_rules) == '오류없음'
