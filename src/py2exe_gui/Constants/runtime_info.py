# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""运行时信息，存储于全局变量 `RUNTIME_INFO` 中

目前包括运行时平台（操作系统）、运行时语言（本地化）、运行时捆绑状态（是否已经被 PyInstaller 打包）
"""

__all__ = [
    "Platform",
    "get_platform",
    "RuntimeInfo",
    "RUNTIME_INFO",
]

import enum
import sys
from locale import getdefaultlocale
from typing import NamedTuple, Optional


@enum.unique
class Platform(enum.Enum):
    """运行平台相关的常量

    由于 enum.StrEnum 在 Python 3.11 才新增，为保持对低版本的支持，暂不使用
    """

    windows = "Windows"
    linux = "Linux"
    macos = "macOS"
    others = "others"


def get_platform() -> Platform:
    """辅助函数，用于获取当前运行的平台

    :return: platform
    """

    if sys.platform.startswith("win32"):
        return Platform.windows
    elif sys.platform.startswith("linux"):
        return Platform.linux
    elif sys.platform.startswith("darwin"):
        return Platform.macos
    else:
        return Platform.others


class RuntimeInfo(NamedTuple):
    """运行时信息数据结构类"""

    platform: Platform  # 运行平台，Windows、macOS、Linux或其他
    language_code: Optional[str]  # 语言环境，zh-CN、en-US 等
    is_bundled: bool  # 是否在已被 PyInstaller 捆绑的冻结环境中运行


# 虽然 locale.getdefaultlocale() 函数已被废弃[https://github.com/python/cpython/issues/90817]，
# 但仍然是目前唯一能在 Windows 平台正确获取语言编码的方式[https://github.com/python/cpython/issues/82986]
# 当 Python 更新修复了这一问题后，将迁移至 locale.getlocale()
language_code = getdefaultlocale()[0]  # noqa

# 判断当前是在普通 Python 环境中运行，还是已被 PyInstaller 捆绑/打包
# https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    is_bundled = True
else:
    is_bundled = False

# 全局变量 RUNTIME_INFO
RUNTIME_INFO = RuntimeInfo(get_platform(), language_code, is_bundled)
