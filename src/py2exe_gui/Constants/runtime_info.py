# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
运行时信息
"""

import sys
from locale import getdefaultlocale
from typing import NamedTuple, Optional

from .platform_constants import PLATFORM, get_platform


class RuntimeInfo(NamedTuple):
    """
    运行时信息数据结构类
    """

    platform: PLATFORM  # 运行平台，Windows、macOS、Linux或其他
    language_code: Optional[str]  # 语言环境，zh-CN、en-US 等
    is_bundled: bool  # 是否在已被 PyInstaller 捆绑的冻结环境中运行


# 虽然 locale.getdefaultlocale() 函数已被废弃[https://github.com/python/cpython/issues/90817]，
# 但仍然是目前唯一能在 Windows 平台正确获取语言编码的方式[https://github.com/python/cpython/issues/82986]
# 当 Python 更新修复了这一问题后，将迁移至 locale.getlocale()
language_code = getdefaultlocale()[0]

# https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    is_bundled = True
else:
    is_bundled = False

RUNTIME_INFO = RuntimeInfo(get_platform(), language_code, is_bundled)
