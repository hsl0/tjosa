"""한국어 조사를 어간에 맞게 자동으로 맞춰주는 라이브러리입니다.

Python 3.14 이상 버전에서 t-string을 통해 삽입한 값의 조사를 자동으로 인식해 변환하는 기능을 지원합니다."""

from sys import version_info
from .josa_only import josa_only


if version_info.major == 3 and version_info.minor >= 14:
    from .josa import josa  # pyright: ignore[reportAssignmentType]

__all__ = ["josa", "josa_only"]
