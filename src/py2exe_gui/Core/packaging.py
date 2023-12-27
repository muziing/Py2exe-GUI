# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from pathlib import Path
from typing import List, Optional

from PySide6 import QtCore

from ..Constants.packaging_constants import PyInstOpt
from .subprocess_tool import SubProcessTool


class Packaging(QtCore.QObject):
    """
    执行打包子进程的类，负责拼接命令选项、设置子进程工作目录、启动子进程等
    不负责输入参数的检查，输入参数检查由 PackagingTask 对象进行 \n
    """

    # 自定义信号
    args_settled = QtCore.Signal(list)  # 所有选项完成设置，直接将命令行参数传出

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.args_dict: dict = dict.fromkeys(PyInstOpt, "")
        self._args: List[str] = []  # PyInstaller 命令
        self._subprocess_working_dir: str = ""
        self.subprocess: SubProcessTool = SubProcessTool("", parent=self)

    @QtCore.Slot(tuple)
    def set_pyinstaller_args(self, arg: tuple[PyInstOpt, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并添加至命令参数字典 \n
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if isinstance(arg_key, PyInstOpt):
            self.args_dict[arg_key] = arg_value
            self._add_pyinstaller_args()
            self._set_subprocess_working_dir()

    def set_python_path(self, python_path):
        """
        :param python_path: Python 可执行文件路径
        """

        self.subprocess.set_program(python_path)

    def _add_pyinstaller_args(self) -> None:
        """
        将命令参数字典中的参数按顺序添加到PyInstaller命令参数列表中 \n
        """

        self._args = []  # 避免重复添加

        self._args.append(self.args_dict[PyInstOpt.script_path])

        if self.args_dict[PyInstOpt.icon_path]:
            self._args.extend(["--icon", self.args_dict[PyInstOpt.icon_path]])

        if self.args_dict[PyInstOpt.add_data]:
            for item in self.args_dict[PyInstOpt.add_data]:
                self._args.extend(["--add-data", f"{item[0]}:{item[1]}"])

        if self.args_dict[PyInstOpt.add_binary]:
            for item in self.args_dict[PyInstOpt.add_binary]:
                self._args.extend(["--add-binary", f"{item[0]}:{item[1]}"])

        if self.args_dict[PyInstOpt.FD]:
            self._args.append(self.args_dict[PyInstOpt.FD])

        if self.args_dict[PyInstOpt.console]:
            self._args.append(self.args_dict[PyInstOpt.console])

        if self.args_dict[PyInstOpt.hidden_import]:
            for item in self.args_dict[PyInstOpt.hidden_import]:
                self._args.extend(["--hidden-import", item])

        if self.args_dict[PyInstOpt.out_name]:
            self._args.extend(["--name", self.args_dict[PyInstOpt.out_name]])

        if self.args_dict[PyInstOpt.clean]:
            self._args.append(self.args_dict[PyInstOpt.clean])

        self.args_settled.emit(self._args)

    def _set_subprocess_working_dir(self) -> None:
        """
        设置子进程工作目录 \n
        """

        script_path = self.args_dict[PyInstOpt.script_path]
        self._subprocess_working_dir = str(Path(script_path).parent)  # 工作目录设置为脚本所在目录

    def run_packaging_process(self) -> None:
        """
        使用给定的参数启动打包子进程 \n
        """

        # 从 Python 内启动 Pyinstaller，
        # 参见 https://pyinstaller.org/en/stable/usage.html#running-pyinstaller-from-python-code
        cmd = [
            "-c",
            f"import PyInstaller.__main__;PyInstaller.__main__.run({self._args})",
        ]

        self.subprocess.set_working_dir(self._subprocess_working_dir)
        self.subprocess.set_arguments(cmd)
        self.subprocess.start_process(
            time_out=500, mode=QtCore.QIODeviceBase.OpenModeFlag.ReadOnly
        )
