from sys import version_info
from .josa_only import josa_only


if version_info.major == 3 and version_info.minor >= 14:
    from .josa import josa  # pyright: ignore[reportAssignmentType]

__all__ = ["josa", "josa_only"]
