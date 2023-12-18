# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
一些因操作系统不同而在具体实现上有差异的功能函数
注意，由于开发者没有苹果电脑，所有关于 macOS 的功能均未经过验证
"""

import subprocess

from ..Constants import PLATFORM, RUNTIME_INFO


def open_dir_in_explorer(dir_path: str) -> None:
    """
    在操作系统文件资源管理器中打开指定目录 \n
    :param dir_path: 待打开的目录路径
    """

    if RUNTIME_INFO.platform == PLATFORM.windows:
        import os  # fmt: skip
        os.startfile(dir_path)  # type: ignore
    elif RUNTIME_INFO.platform == PLATFORM.linux:
        subprocess.call(["xdg-open", dir_path])
    elif RUNTIME_INFO.platform == PLATFORM.macos:
        subprocess.call(["open", dir_path])


def get_sys_python() -> str:
    """
    获取系统默认 Python 解释器的可执行文件位置 \n
    :return: Python 可执行文件路径
    """

    if RUNTIME_INFO.platform == PLATFORM.windows:
        cmd = "powershell.exe (Get-Command python).Path"  # PowerShell
    elif RUNTIME_INFO.platform in (PLATFORM.linux, PLATFORM.macos):
        cmd = "which python3"
    else:
        raise ValueError("Current OS is not supported.")

    return subprocess.getoutput(cmd)
