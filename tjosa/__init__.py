from sys import version_info, _getframe
from .josa_only import josa_only


def _is_josa_only_import():
    # 현재 실행 스택을 역으로 훑습니다.
    frame = _getframe()
    while frame:
        # importlib의 내부 로딩 함수를 찾습니다.
        if frame.f_code.co_name in ("_find_and_load", "_find_and_load_unlocked"):
            target_name = frame.f_locals.get("name")
            # 만약 현재 로드 프로세스의 최종 타겟이 'josa_only' 경로라면
            if target_name == "tjosa.josa_only":
                return True
        frame = frame.f_back
    return False


if version_info.major == 3 and version_info.minor >= 14:
    from .josa import josa  # pyright: ignore[reportAssignmentType]
else:
    import warnings

    if not _is_josa_only_import():
        warnings.warn(
            f"""
tjosa 패키지는 Python 3.14 이상 버전을 권장합니다.
이전 버전에서도 일부 기능을 지원하지만, 일부 핵심 기능은 사용할 수 없습니다.

현재 Python 버전은 {version_info.major}.{version_info.minor} 입니다.

josa() 함수는 t-string을 요구하므로 현재 사용할 수 없습니다.
josa_only() 함수는 구 버전 Python에서도 사용할 수 있습니다.

이 메시지를 숨기려면 'tjosa' 모듈 대신 'tjosa.josa_only' 모듈을 사용해 주세요.
""",
        )

__all__ = ["josa", "josa_only"]
