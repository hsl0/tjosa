"""공통 타입 정의"""

# 조사 튜플 타입
type Josa[T: str = str, U: str = T] = tuple[T, U]
