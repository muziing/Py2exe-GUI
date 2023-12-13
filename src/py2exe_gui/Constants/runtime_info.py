# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
运行时信息
"""

from locale import getdefaultlocale
from typing import NamedTuple, Optional

from .platform_constants import PLATFORM, get_platform


class RuntimeInfo(NamedTuple):
    platform: PLATFORM
    language_code: Optional[str]


# 虽然 locale.getdefaultlocale() 函数已被废弃[https://github.com/python/cpython/issues/90817]，
# 但仍然是目前唯一能在 Windows 平台正确获取语言编码的方式[https://github.com/python/cpython/issues/82986]
# 当 Python 更新修复了这一问题后，将迁移至 locale.getlocale()
RUNTIME_INFO = RuntimeInfo(get_platform(), getdefaultlocale()[0])  # noqa
