"""
打包相关的常量
"""

# TODO 优化打包选项列表的数据结构

pyinstaller_args_list: list = [
    "script_path",
    "icon_path",
    "FD",
    "console",
    "out_name",
]


class PyinstallerArgs:
    script_path = "script_path"
    icon_path = "icon_path"
    FD = "FD"
    console = "console"
    out_name = "out_name"
