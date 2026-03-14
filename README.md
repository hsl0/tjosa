# tjosa

한국어 조사를 어간에 맞게 자동으로 맞춰주는 라이브러리입니다. t-string을 통해 삽입한 값의 조사를 자동으로 인식해 변환하는 기능을 지원합니다.

## 요구 사항 (Requirements)

- Python 3.14+

## 설치 방법 (Installation)

```bash
pip install tjosa
```

## 지원 조사

- 은/는
- 이/가
- 을/를
- 과/와
- 으로/로
- 아/야
- 이/
  - 이랑/랑
  - 이며/며
  - 이다/다
  - 이가/가

`이랑/랑`, `이며/며`, `이다/다`, `이가/가`는 `이/`를 통해 지원합니다.

## 사용법 (Usage)

### josa

`josa(template: Template, *, custom_josas: Sequence[tuple[str, str]], unused_josas: Sequence[str]) -> str`

t-string 템플릿의 삽입값에 맞춰 뒤따르는 조사를 자동 변환합니다.

`custom_josas` 변수에 (받침 있음, 받침 없음)을 매핑한 사용자 지정 조사 튜플의 목록을 넣으면 해당 조사도 변환합니다.

`unused_josas` 변수에 변환하기를 원치 않는 조사의 목록을 입력할 수 있습니다.

예시:

```python
from tjosa import josa

food = "사과"
print(josa(t"{food}는 맛있다"))   # 사과는 맛있다

food = "파인애플"
print(josa(t"{food}는 맛있다"))   # 파인애플은 맛있다

```

### josa_only

`josa_only(eogan: str, josa: str | tuple[str, str]) -> str`

어간과 조사를 입력하면, 어간에 맞는 적절한 조사를 반환합니다.

`josa`에 입력할 수 있는 조사는 [지원 조사](#지원-조사) 문단을 참고해 주세요. 예를 들어, `은/는`을 사용할 경우 `은` 또는 `는` 중 하나를 선택해서 `josa` 인자이 입력하면 됩니다.

단, `이/가`와 `이/`와 중복되는 조사 `이`의 경우, `이/`가 우선되므로 `이/가`를 구분하려는 경우에는 `가`를 사용해 주세요.

`josa`에 (받침 있음, 받침 없음)을 매핑한 사용자 지정 조사 튜플을 대신 사용할 수 있습니다.

예시:

- `josa_only("사과", "은")` -> `는`
- `josa_only("집", "은")` -> `은`
- `josa_only("학교", "으로")` -> `로`

## 라이선스 (License)

MIT (예정)
