# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import sys
from enum import Enum, unique


@unique
class PLATFORM(Enum):
    """
    运行平台相关的常量 \n
    """

    windows = "Windows"
    linux = "Linux"
    macos = "macOS"
    others = "others"


def get_platform() -> PLATFORM:
    """
    辅助函数，用于获取当前运行的平台 \n
    :return: platform
    """

    if sys.platform.startswith("win32"):
        return PLATFORM.windows
    elif sys.platform.startswith("linux"):
        return PLATFORM.linux
    elif sys.platform.startswith("darwin"):
        return PLATFORM.macos
    else:
        return PLATFORM.others
