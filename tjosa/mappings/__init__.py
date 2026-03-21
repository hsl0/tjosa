"""변환 규칙 매핑 모듈"""

from .ConversionMap import create_conversion_map, ConversionMap
from .josa import josa_map, BuiltinJosa

__all__ = ["create_conversion_map", "josa_map", "BuiltinJosa", "ConversionMap"]
