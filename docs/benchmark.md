# 조사 처리 라이브러리 비교 벤치마크

시행일: 2026-03-15  
환경: Windows / Python 3.14.3 / pytest-benchmark 5.2.3

## 측정 방법

- 명령:
  - `py -m pytest test/perftest.py -m replace --benchmark-only -q`
  - `py -m pytest test/perftest.py -m select --benchmark-only -q`
- 각 그룹을 **10회 반복** 실행
- 단위: 마이크로초(μs), 낮을수록 빠름
- 가설 검정 유의수준: **α = 0.05** (95% 신뢰구간)
- 검정 적용 기준:
  - 동일한 장치에서 인접한 시점에 반복 측정하므로, 각 비교군의 결과는 하드웨어 상태 및 백그라운드 환경의 변동을 함께 겪어 쌍체(대응표본) 구조로 간주한다.
  - Shapiro-Wilk로 **쌍체 차이값 D = (tjosa - 비교군)** 정규성 확인
  - `p(D) ≥ 0.05` 이면 단측 paired t-test를 1차 검정으로 사용
  - `p(D) < 0.05` 이면 단측 Wilcoxon signed-rank test를 1차 검정으로 사용

## 비교군

### Replace 그룹

문장 전체 조사 변환 함수

- hsl0/tjosa.josa
- [myevan/pyjosa](github.com/myevan/pyjosa).replace_josa

### Select 그룹

단일 단어 조사 판별 함수

- hsl0/tjosa.josa_only
- [kimsewhan96/pyjosa](github.com/kimsewhan96/pyjosa).get_josa 1.0.3
- [hyunwoongko/kss](github.com/hyunwoongko/kss).select_josa 6.0.6
- [what-studio/tossi](what-studio/tossi).pick 0.3.1

## 결과

### Replace 그룹

| 테스트 | Mean(avg) μs | Run variation μs | Range (min~max) μs | Fastest wins |
|---|---:|---:|---:|---:|
| test_tjosa_josa | 32.1564 | 0.7686 | 31.2007 ~ 33.7886 | 10/10 |
| test_myevan_pyjosa_replace_josa | 37.2463 | 3.9454 | 34.5226 ~ 48.8489 | 0/10 |

#### `hsl0/tjosa.josa` vs `myevan/pyjosa.replace_josa`

- 귀무가설 H0: `hsl0/tjosa.josa`는 `myevan/pyjosa.replace_josa`보다 빠르지 않다.
  ($\mu_{a} - \mu_{b} \ge 0$)
- 대립가설 H1: `hsl0/tjosa.josa`는 `myevan/pyjosa.replace_josa`보다 빠르다.
  ($\mu_{a} - \mu_{b} \lt 0$)
- 평균 차이: **-5.0899 μs** (`hsl0/tjosa.josa`가 빠름)
- 상대 차이: **-13.67%**
- 런별 승패: `hsl0/tjosa.josa` 빠름 **10/10**, 느림 **0/10**
- 정규성(Shapiro-Wilk):
  - `hsl0/tjosa.josa` p=**0.349639**
  - `myevan/pyjosa.replace_josa` p=**0.000015**
  - 차이값 D p=**0.000005** → 정규성 가정 불충족
- 검정 p-value (단측 Wilcoxon signed-rank): **0.0009765625**
- 참고 p-value (단측 paired t-test): **0.0010413585**
- 가설 판정(α=0.05): **H0 기각, H1 채택**

문장 전체 조사 변환 유즈케이스에서는 `hsl0/tjosa.josa`가 통계적으로 유의하게 우세.

---

### 3.2 Select 그룹

| 테스트 | Mean(avg) μs | Run variation μs | Range (min~max) μs |
|---|---:|---:|---:|
| test_tjosa_josa_only | 8.9497 | 0.4107 | 8.3563 ~ 9.8005 |
| test_kimsewhan96_pyjosa_get_josa | 26.0833 | 1.5565 | 24.4292 ~ 29.1648 |
| test_tossi_pick | 78.8639 | 3.1455 | 75.5816 ~ 86.0720 |
| test_kss_select_josa | 111.0664 | 6.6469 | 103.8600 ~ 126.9704 |

#### `hsl0/tjosa.josa_only` vs `kimsewhan96/pyjosa.get_josa`

- 귀무가설 H0: `hsl0/tjosa.josa_only`는 `kimsewhan96/pyjosa.get_josa`보다 빠르지 않다.
  ($\mu_{a} - \mu_{b} \ge 0$)
- 대립가설 H1: `hsl0/tjosa.josa_only`는 `kimsewhan96/pyjosa.get_josa`보다 빠르다.
  ($\mu_{a} - \mu_{b} \lt 0$)
- 평균 차이: **-17.1335 μs** (`hsl0/tjosa.josa_only`가 빠름)
- 상대 차이: **-65.69%**
- 런별 승패: `hsl0/tjosa.josa_only` 빠름 **10/10**
- 정규성(Shapiro-Wilk):
  - `hsl0/tjosa.josa_only` p=**0.734057**
  - `kimsewhan96/pyjosa.get_josa` p=**0.130141**
  - 차이값 D p=**0.598621** → 정규성 가정 충족
- 검정 p-value (단측 paired t-test): **0.0000000001**
- 참고 p-value (단측 Wilcoxon signed-rank): **0.0009765625**
- 가설 판정(α=0.05): **H0 기각, H1 채택**

단일 단어 조사 판별 유즈케이스에서는 `hsl0/tjosa.josa_only`가 통계적으로 유의하게 우세.

## 종합 결론

- `tjosa`는 기능 분리 관점에서 성능 포지션이 명확하다.
  - **조사 선택 전용(`josa_only`)**: 최상위권 성능 (이번 측정에선 `pyjosa` 대비 큰 폭 우세)
  - **문자열 치환 포함(`josa`)**: `replace` 조건(현재 비교군 `myevan`)에서 비모수 1차 검정 기준 통계적으로 유의한 우세
- 두 핵심 비교쌍 모두에서 귀무가설(H0)을 기각했고, `tjosa`가 더 빠르다는 대립가설(H1)을 채택했다.

## 비고

- 본 보고서는 비교군 구성이 업데이트된 시점의 최신 재측정 결과를 반영한다.
- `replace`는 전체 문자열 변환 API끼리의 비교를 우선한다.
- `select`는 조사 선택 엔진 성능 비교 지표로 분리 해석한다.

## 주의사항

- 마이크로벤치는 OS 스케줄링/백그라운드 프로세스 영향이 있다.
- 절대값보다 반복 측정 집계(평균, 변동성, 유의수준 기반 가설 판정)를 기준으로 해석해야 한다.
- 이번 보고서는 동일 머신/동일 환경에서의 상대 비교 결과다.
