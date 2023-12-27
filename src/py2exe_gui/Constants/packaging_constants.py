# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
打包相关的常量
"""

import enum


@enum.unique
class PyInstOpt(enum.IntFlag):
    """
    PyInstaller 命令行选项枚举类
    """

    script_path = enum.auto()
    icon_path = enum.auto()
    FD = enum.auto()
    console = enum.auto()
    out_name = enum.auto()
    add_data = enum.auto()
    add_binary = enum.auto()
    hidden_import = enum.auto()
    clean = enum.auto()
