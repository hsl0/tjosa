'''유사 라이브러리 간 속도 비교

py -m pytest test/perftest.py --benchmark-only

출처: kimsehwan96/pyjosa (MIT 라이선스)
     https://github.com/kimsehwan96/pyjosa/blob/master/performance_test.py
'''

# pylint: disable=import-outside-toplevel

import pytest

word_list = ["오리", "예나", "세환", "철수", "길동", "우주"]
possible_results = {
    '은는': ['오리는', '예나는', '세환은', '철수는', '길동은', '우주는'],
    '이가': ['오리가', '예나가', '세환이', '철수가', '길동이', '우주가'],
    '과와': ['오리와', '예나와', '세환과', '철수와', '길동과', '우주와'],
    '을를': ['오리를', '예나를', '세환을', '철수를', '길동을', '우주를']
}
josa_answer = {
    '은는': {'오리': '는', '예나': '는', '세환': '은', '철수': '는', '길동': '은', '우주': '는'},
    '이가': {'오리': '가', '예나': '가', '세환': '이', '철수': '가', '길동': '이', '우주': '가'},
    '과와': {'오리': '와', '예나': '와', '세환': '과', '철수': '와', '길동': '과', '우주': '와'},
    '을를': {'오리': '를', '예나': '를', '세환': '을', '철수': '를', '길동': '을', '우주': '를'},
}

@pytest.mark.replace
def test_tjosa_josa(benchmark):
    '''tjosa.josa 테스트'''

    from tjosa import josa

    def run():
        for word in word_list:
            assert josa(t"{word}는") in possible_results['은는']
            assert josa(t"{word}가") in possible_results['이가']
            assert josa(t"{word}과") in possible_results['과와']
            assert josa(t"{word}를") in possible_results['을를']

    benchmark(run)


@pytest.mark.select
def test_tjosa_josa_only(benchmark):
    '''tjosa.josa_only 테스트'''

    from tjosa import josa_only

    def run():
        for word in word_list:
            assert josa_only(word, "은") == josa_answer['은는'][word]
            assert josa_only(word, "가") == josa_answer['이가'][word]
            assert josa_only(word, "와") == josa_answer['과와'][word]
            assert josa_only(word, "를") == josa_answer['을를'][word]

    benchmark(run)


@pytest.mark.select
def test_kimsewhan96_pyjosa_get_josa(benchmark):
    '''kimsewhan96/pyjosa.get_josa 테스트'''
    from pyjosa.josa import Josa

    def run():
        for word in word_list:
            assert Josa.get_josa(word, "은") == josa_answer['은는'][word]
            assert Josa.get_josa(word, "가") == josa_answer['이가'][word]
            assert Josa.get_josa(word, "와") == josa_answer['과와'][word]
            assert Josa.get_josa(word, "를") == josa_answer['을를'][word]

    benchmark(run)


@pytest.mark.select
def test_kss_select_josa(benchmark):
    '''kss.select_josa 테스트'''

    from kss import Kss

    select_josa = Kss("select_josa")

    def run():
        for word in word_list:
            assert select_josa(word, "은") == josa_answer['은는'][word]
            assert select_josa(word, "가") == josa_answer['이가'][word]
            assert select_josa(word, "와") == josa_answer['과와'][word]
            assert select_josa(word, "를") == josa_answer['을를'][word]

    benchmark(run)


@pytest.mark.select
def test_tossi_pick(benchmark):
    '''tossi.pick 테스트'''

    import tossi

    def run():
        for word in word_list:
            assert tossi.pick(word, "은") == josa_answer['은는'][word]
            assert tossi.pick(word, "가") == josa_answer['이가'][word]
            assert tossi.pick(word, "와") == josa_answer['과와'][word]
            assert tossi.pick(word, "를") == josa_answer['을를'][word]

    benchmark(run)

# pylint: disable=invalid-name


def myevan_pyjosa():
    '''myevan/pyjosa 모듈 생성'''

    import re

    JOSA_PAIRD = {
        "(이)가": ("이", "가"),
        "(와)과": ("과", "와"),
        "(을)를": ("을", "를"),
        "(은)는": ("은", "는"),
        "(으)로": ("으로", "로"),
        "(아)야": ("아", "야"),
        "(이)여": ("이여", "여"),
        "(이)라": ("이라", "라"),
    }

    JOSA_REGEX = re.compile(
        r"\(이\)가|\(와\)과|\(을\)를|\(은\)는|\(아\)야|\(이\)여|\(으\)로|\(이\)라"
    )

    def choose_josa(prev_char, josa_key, josa_pair):
        """
        조사 선택
        :param prev_char 앞 글자
        :param josa_key 조사 키
        :param josas 조사 리스트
        """
        char_code = ord(prev_char)

        # 한글 코드 영역(가 ~ 힣) 아닌 경우
        if char_code < 0xAC00 or char_code > 0xD7A3:
            return josa_pair[1]

        local_code = char_code - 0xAC00  # '가' 이후 로컬 코드
        jong_code = local_code % 28

        # 종성이 없는 경우
        if jong_code == 0:
            return josa_pair[1]

        # 종성이 있는 경우
        if josa_key == "(으)로":
            if jong_code == 8:  # ㄹ 종성인 경우
                return josa_pair[1]

        return josa_pair[0]

    def replace_josa(src):
        tokens = []
        base_index = 0
        for mo in JOSA_REGEX.finditer(src):
            prev_token = src[base_index: mo.start()]
            prev_char = prev_token[-1]
            tokens.append(prev_token)

            josa_key = mo.group()
            tokens.append(choose_josa(
                prev_char, josa_key, JOSA_PAIRD[josa_key]))

            base_index = mo.end()

        tokens.append(src[base_index:])
        return "".join(tokens)

    return {'choose_josa': choose_josa, 'replace_josa': replace_josa}
# pylint: enable=invalid-name


@pytest.mark.replace
def test_myevan_pyjosa_replace_josa(benchmark):
    '''myevan/pyjosa.replcae_josa 테스트'''

    replace_josa = myevan_pyjosa()['replace_josa']

    def run():
        for word in word_list:
            assert replace_josa(f"{word}(은)는") in possible_results['은는']
            assert replace_josa(f"{word}(이)가") in possible_results['이가']
            assert replace_josa(f"{word}(와)과") in possible_results['과와']
            assert replace_josa(f"{word}(을)를") in possible_results['을를']

    benchmark(run)
