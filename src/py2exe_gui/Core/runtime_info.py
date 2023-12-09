# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
运行时信息
"""

from locale import LC_CTYPE, getlocale
from typing import NamedTuple, Optional

from ..Constants import PLATFORM, get_platform


class RuntimeInfo(NamedTuple):
    platform: PLATFORM
    language_code: Optional[str]


RUNTIME_INFO = RuntimeInfo(get_platform(), getlocale(category=LC_CTYPE)[0])
