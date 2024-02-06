# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""一些因操作系统不同而在具体实现上有差异的功能函数

注意，由于开发者没有苹果电脑，所有 macOS 功能均未经过验证
"""

__all__ = [
    "open_dir_in_explorer",
    "get_sys_python",
    "get_user_config_dir",
    "get_user_cache_dir",
    "get_venv_python",
]

import subprocess
import warnings
from pathlib import Path
from typing import Union

from ..Constants import RUNTIME_INFO, Platform


def open_dir_in_explorer(dir_path: Union[str, Path]) -> None:
    """在操作系统文件资源管理器中打开指定目录

    :param dir_path: 待打开的目录路径
    :raise RuntimeError: 当前操作系统不受支持时抛出
    """

    try:
        if RUNTIME_INFO.platform == Platform.windows:
            import os  # fmt: skip
            os.startfile(dir_path)  # type: ignore
        elif RUNTIME_INFO.platform == Platform.linux:
            subprocess.call(["xdg-open", dir_path])
        elif RUNTIME_INFO.platform == Platform.macos:
            subprocess.call(["open", dir_path])
        else:
            raise RuntimeError("Current OS is not supported.")
    except OSError as e:
        warnings.warn(
            f"Error occurred while trying to open directory in explorer: {e}",
            RuntimeWarning,
            stacklevel=2,
        )


def get_sys_python() -> str:
    """获取系统默认 Python 解释器的可执行文件位置

    :return: Python 可执行文件路径
    :raise RuntimeError: 当前操作系统不受支持时抛出
    :raise FileNotFoundError: 未找到 Python 解释器抛出
    """

    if RUNTIME_INFO.platform == Platform.windows:
        cmd = ["powershell.exe", "(Get-Command python).Path"]  # PowerShell
    elif RUNTIME_INFO.platform in (Platform.linux, Platform.macos):
        cmd = ["which", "python3"]
    else:
        raise RuntimeError("Current OS is not supported.")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        python_path = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        warnings.warn(
            f"Error occurred while trying to get system default Python interpreter: {e.output}",
            RuntimeWarning,
            stacklevel=2,
        )
        raise

    if not Path(python_path).exists():
        raise FileNotFoundError(f"Python interpreter not found: {python_path}")

    return python_path


def get_user_config_dir() -> Path:
    """获取当前平台用户配置文件目录路径

    :return: 用户配置文件目录路径
    :raise RuntimeError: 当前操作系统不受支持时抛出
    """

    if RUNTIME_INFO.platform == Platform.windows:
        return Path.home() / "AppData" / "Roaming"
    elif RUNTIME_INFO.platform == Platform.linux:
        return Path.home() / ".config"
    elif RUNTIME_INFO.platform == Platform.macos:
        return Path.home() / "Library" / "Application Support"
    else:
        raise RuntimeError("Current OS is not supported.")


def get_user_cache_dir() -> Path:
    """获取当前平台用户缓存或数据文件目录路径

    :return: 用户缓存目录路径
    :raise RuntimeError: 当前操作系统不受支持时抛出
    """

    if RUNTIME_INFO.platform == Platform.windows:
        return Path.home() / "AppData" / "Local"
    elif RUNTIME_INFO.platform == Platform.linux:
        return Path.home() / ".cache"
    elif RUNTIME_INFO.platform == Platform.macos:
        return Path.home() / "Library" / "Caches"
    else:
        raise RuntimeError("Current OS is not supported.")


def get_venv_python(root_path: Union[str, Path]) -> Path:
    """获取当前平台 venv 虚拟环境中 Python 解释器的可执行文件位置

    :param root_path: venv 虚拟环境根路径
    :return: Python 可执行文件路径
    :raise RuntimeError: 当前操作系统不受支持时抛出
    """

    root = Path(root_path)

    if RUNTIME_INFO.platform == Platform.windows:
        return root / "Scripts" / "python.exe"
    elif RUNTIME_INFO.platform in (Platform.linux, Platform.macos):
        return root / "bin" / "python3"
    else:
        raise RuntimeError("Current OS is not supported.")
