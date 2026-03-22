"""조사 판정 불가 시 사용되는 폴백 포맷터 관련 모듈"""

from .FallbackFormatter import FallbackFormatter
from .format_fallback import format_fallback

__all__ = ["FallbackFormatter", "format_fallback"]
