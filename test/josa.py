'''josa 함수에 대한 테스트'''

from tjosa import josa


def test_english():
    assert josa(t'{"Test"}이 진행 중입니다.') == 'Test이(가) 진행 중입니다.'
    assert josa(t'현재 상태는 {"Testing"}이다.') == '현재 상태는 Testing(이)다.'

def test_custom_josas():
    custom_josas = [('있', '없')]
    assert josa(t'{"받침"}있음', custom_josas=custom_josas) == '받침있음'
    assert josa(t'{"오류"}있음', custom_josas=custom_josas) == '오류없음'
