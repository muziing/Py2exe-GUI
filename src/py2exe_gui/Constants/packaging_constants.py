# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""
打包相关的常量
"""

import enum


@enum.unique
class PyinstallerArgs(enum.IntFlag):
    script_path = enum.auto()
    icon_path = enum.auto()
    FD = enum.auto()
    console = enum.auto()
    out_name = enum.auto()
