# tjosa

한국어 조사를 어간에 맞게 자동으로 맞춰주는 라이브러리입니다. t-string을 통해 삽입한 값의 조사를 자동으로 인식해 변환하는 기능을 지원합니다.

## 요구 사항 (Requirements)

- Python 3.12+
  - t-string을 기반한 `josa()` 함수는 Python 3.14 이상 버전 필요
  - Python 3.14 미만 버전에서는 `josa_only()` 함수만 사용 가능

## 설치 방법 (Installation)

```bash
pip install tjosa
```

## 지원 조사

- [은](https://stdict.korean.go.kr/search/searchView.do?word_no=467516&searchKeywordTo=3)/[는](https://stdict.korean.go.kr/search/searchView.do?word_no=406525&searchKeywordTo=3)
- [이](https://stdict.korean.go.kr/search/searchView.do?word_no=471254&searchKeywordTo=3)/[가](https://stdict.korean.go.kr/search/searchView.do?word_no=382734&searchKeywordTo=3)
- [을](https://stdict.korean.go.kr/search/searchView.do?word_no=469161&searchKeywordTo=3)/[를](https://stdict.korean.go.kr/search/searchView.do?word_no=421993&searchKeywordTo=3)
- [과](https://stdict.korean.go.kr/search/searchView.do?word_no=398563&searchKeywordTo=3)/[와](https://stdict.korean.go.kr/search/searchView.do?word_no=249573&searchKeywordTo=3)
- [으로](https://stdict.korean.go.kr/search/searchView.do?word_no=473314&searchKeywordTo=3)/[로](https://stdict.korean.go.kr/search/searchView.do?word_no=421619&searchKeywordTo=3)
- [아](https://stdict.korean.go.kr/search/searchView.do?word_no=216454&searchKeywordTo=3)/[야](https://stdict.korean.go.kr/search/searchView.do?word_no=220409&searchKeywordTo=3)
- [이](https://stdict.korean.go.kr/search/searchView.do?word_no=267418&searchKeywordTo=3)/
  - [이랑](https://stdict.korean.go.kr/search/searchView.do?word_no=469683&searchKeywordTo=3)/[랑](https://stdict.korean.go.kr/search/searchView.do?word_no=100236&searchKeywordTo=3)
  - [이며](https://stdict.korean.go.kr/search/searchView.do?word_no=260127&searchKeywordTo=3)/[며](https://stdict.korean.go.kr/search/searchView.do?word_no=425032&searchKeywordTo=3)
  - 이다/다
  - 이가/가

`이랑/랑`, `이며/며`, `이다/다`, `이가/가`는 `이/`를 통해 지원합니다.

## 사용법 (Usage)

### josa

`josa(template: Template, *, conversion_rules: ConversionMap[str], fallback_formatter: FallbackFormatter[str]) -> str`

t-string 템플릿의 삽입값에 맞춰 뒤따르는 조사를 자동 변환합니다.

**Python 3.14 이상 버전이 필요합니다.**

`conversion_rules` 변수에 `ConversionRule` 클래스 기반의 변환 규칙들을 포함한 `ConversionMap`을 넣어 변환 규칙을 변경할 수 있습니다.

`fallback_formatter` 변수에 `FallbackFormatter` 프로토콜을 따르는 함수를 넣어 조사 판별 불가 시 `이(가)`와 같이 대체되는 문자열의 형식을 바꿀 수 있습니다.

예시:

```python
from tjosa import josa

food = "사과"
print(josa(t"{food}는 맛있다"))   # 사과는 맛있다

food = "파인애플"
print(josa(t"{food}는 맛있다"))   # 파인애플은 맛있다

```

### josa_only

`josa_only(cheon: str, josa: BuiltinJosa | ConversionRule[str] | str, *, fallback_formatter: FallbackFormatter[F],conversion_rules: ConversionMap[str]) -> str`

체언과 조사를 입력하면, 체언에 맞는 적절한 조사를 반환합니다.

`josa`에 입력할 수 있는 조사는 [지원 조사](#지원-조사) 문단을 참고해 주세요. 예를 들어, `은/는`을 사용할 경우 `은` 또는 `는` 중 하나를 선택해서 `josa` 인자에 입력하면 됩니다.

단, `이/가`와 `이/`와 중복되는 조사 `이`의 경우, `이/`가 우선되므로 `이/가`를 구분하려는 경우에는 `가`를 사용해 주세요.

`josa`에 `ConversionRule` 클래스를 사용한 사용자 지정 조사 변환 규칙 객체를 대신 사용할 수 있습니다.

예시:

- `josa_only("사과", "은")` -> `는`
- `josa_only("집", "은")` -> `은`
- `josa_only("학교", "으로")` -> `로`

### 사용자 지정 조사 변환

tjosa 패키지는 사용자 지정 조사 변환 규칙을 추가하거나 변경할 수 있습니다.

예를 들어, 체언의 마지막 음절에 종성(받침)이 존재할 때 '이다', 존재하지 않을 때 '다' 조사를 붙인다면 다음과 같이 사용할 수 있습니다. ('이다/다'는 사용자 지정 규칙 없이도 '이/'를 통해 이미 지원합니다.)

```py
from tjosa import josa
from tjosa.rules import JongsungRule
from tjosa.mappings import create_conversion_map
from tjosa.mappings.josa import josa_rules

e_da = JongsungRule("이다", "다")

custom_josa_map_exclusive = create_conversion_map([e_da])
custom_josa_map_extended = create_conversion_map([*josa_rules, e_da])

word = '조사'
josa(t'{word}이다', conversion_rules=custom_josa_map_exclusive) # 조사다

word = '한글'
josa(t'{word}이다', conversion_rules=custom_josa_map_extended) # 한글이다
```

#### tjosa.mappings 모듈

사용자 지정 조사 쌍 매핑을 만들 수 있는 모듈입니다.

##### ConversionMap

사용 가능한 여러 조사 변환 규칙(`ConversionRule`)들을 묶는 객체입니다.

##### create_conversion_map

`create_conversion_map(rules: ConversionRule[str]) -> ConversionMap[str]`

`ConversionMap` 객체를 생성합니다. 중복된 조사를 등록할 경우, 뒤에 오는 규칙이 우선됩니다.

##### tjosa.mappings.josa 모듈

기본적으로 사용하는 `ConversionMap` 데이터가 있습니다. 사용자 지정 조사 규칙을 추가하거나 일부 규칙을 수정할 때 사용할 수 있습니다.

- `BuiltinJosa`: 기본적으로 제공하는 조사의 리터럴 타입입니다. 타입 검사에서 기본 조사만을 받으려 할 때 사용할 수 있습니다.
- `josa_rules`: 기본적으로 사용하는 조사들의 `ConversionRule` 규칙 객체들을 모아 놓은 리스트입니다. 이 리스트에서 일부 규칙을 수정하거나 사용자 지정 규칙을 추가한 뒤, `create_conversion_map`을 통해 사용자 지정 규칙을 만들 수 있습니다.
- `josa_map`: 기본적으로 사용하는 조사들의 `ConversionMap` 객체입니다.

#### tjosa.rules 모듈

사용자 지정 조사 변환 규칙을 만들 수 있는 모듈입니다.

##### ConversionRule

사용자 지정 조사 변환 규칙을 만들 수 있는 클래스 프로토콜입니다.

변환 규칙이 특수한 조사 쌍을 만들 때 이 프로토콜을 구현한 클래스를 만들 수 있습니다.

`choose()` 메소드와 `get_candidates()` 메소드를 구현해야 합니다.

###### choose

`choose(self, word: str, *, fallback_formatter: FallbackFormatter[str]) -> str`

체언을 입력받아 적절한 조사를 반환합니다.

적절한 조사를 찾지 못한 경우, `fallback_formatter`에 `FallbackFormatter` 인터페이스를 구현한 폴백 포맷터 함수를 이용해 모든 조사 후보를 대신 반환해야 합니다.

###### get_candidates

`get_candidates(self) -> Iterable[str]`

가능한 모든 조사의 후보를 반환합니다.

##### JongsungRule

체언의 마지막 음절에 종성(받침)이 존재하는 지 여부를 바탕으로 조사를 선택합니다.

`JongsungRule(with_jongsung: str, without_jongsung: str)```

`with_jongsung` 인자에 종성이 있을 때 사용할 조사를, `without_jongsung` 인자에 종성이 없을 때 사용할 조사를 입력합니다.

##### JongsungExceptRieulRule

`JongsungRule`과 유사하게 체언의 마지막 음절에 종성(받침)이 존재하는 지 여부를 바탕으로 조사를 선택하지만, 종성이 'ㄹ'일 경우는 예외적으로 종성이 없는 것으로 취급합니다.

`JongsungExceptRieulRule(with_jongsung: str, without_jongsung: str)`

`with_jongsung` 인자에 'ㄹ'이 아닌 종성이 있을 때 사용할 조사를, `without_jongsung` 인자에 종성이 없거나 'ㄹ' 받침이 있을 때 사용할 조사를 입력합니다.

### 사용자 지정 포맷터

한글이 아닌 등 조사를 판별할 수 없을 때 `이(가)` 또는 `(이)`와 같이 조사 중 하나를 괄호에 넣고 둘을 병기합니다. 하지만 `FallbackFormatter` 인터페이스를 구현한 폴백 포맷터 함수를 직접 만들고 `josa()` 함수나 `josa_only()` 함수의 `fallback_formatter` 인자에 넣어 형식을 바꿀 수 있습니다.

```py
from tjosa import josa

def custom_formatter(*candidates: str) -> str:
    return f'({candidates[0]}/{candidates[1]})'

word = 'tjosa'
josa(t'{word}는 좋다.', fallback_formatter=custom_formatter) # tjosa(은/는) 좋다.
```

#### tjosa.formatter 모듈

##### FallbackFormatter

`(*candidates: str) -> str`

사용자 지정 포맷터 함수를 만들 때 준수해야 하는 함수 프로토콜 입니다.

##### format_fallback

`format_fallback(*candidates: str) -> str`

한글이 아닌 등 조사를 판별할 수 없을 때 `이(가)` 또는 `(이)`와 같이 조사 중 하나를 괄호에 넣고 둘을 병기합니다. 기본적으로 사용되는 `FallbackFormatter` 함수입니다.

한 가지 종류의 조사가 들어오면 그 조사를 괄호에 넣습니다. (예: `(이)`)

두 가지 종류의 조사가 들어오면 첫번째 조사는 그대로 표시하고, 두번째 조사는 괄호에 넣어 병기합니다. (예: `이(가)`)

만약 세 가지 이상의 조사가 들어오면 두 가지 종류의 조사가 들어올 때와 같이 표시되며, 세번째 이후의 조사는 무시됩니다.

## 성능 비교 (Performance)

`tjosa`는 한 단어 조사 선택(`josa_only`)과 문장 전체 문자열 변환(`josa`) 사용 방식 모두에서 유사 라이브러리 대비 빠른 성능을 보입니다.

동일 환경에서 유사 라이브러리와 함께 벤치마크를 측정한 결과는 다음과 같습니다.

- 한 단어 조사 선택
  - hsl0/tjosa.josa_only: 평균 **8.9497μs**
  - [kimsehwan96/pyjosa](github.com/kimsehwan96/pyjosa).get_josa: 평균 **26.0833μs**
  - hsl0/tjosa.josa_only가 약 **65.69%** 더 빠름

- 문장 전체 조사 변환
  - hsl0/tjosa.josa: 평균 **32.1564μs**
  - [myevan/pyjosa](github.com/myevan/pyjosa).replace_josa: 평균 **37.2463μs**
  - hsl0/josa가 약 **13.67%** 더 빠름

자세한 사항은 [docs/benchmark.md](./docs/benchmark.md) 문서를 참고해 주세요.

## 라이선스 (License)

본 패키지는 MIT 라이선스로 배포됩니다.
