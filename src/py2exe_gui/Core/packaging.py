# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from pathlib import Path
from typing import List, Optional

from PySide6 import QtCore

from ..Constants.packaging_constants import PyinstallerArgs
from .subprocess_tool import SubProcessTool


class Packaging(QtCore.QObject):
    """
    执行打包子进程的类
    不负责输入参数的检查 \n
    """

    # 自定义信号
    args_settled = QtCore.Signal(list)  # 所有选项完成设置，直接将命令行参数传出

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(Packaging, self).__init__(parent)

        self.args_dict: dict = dict.fromkeys(PyinstallerArgs, "")
        self._args: List[str] = []
        self._subprocess_working_dir: str = ""
        self.subprocess: SubProcessTool = SubProcessTool("pyinstaller", parent=self)

    @QtCore.Slot(tuple)
    def set_pyinstaller_args(self, arg: tuple[PyinstallerArgs, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并添加至命令参数字典 \n
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if type(arg_key) == PyinstallerArgs:
            self.args_dict[arg_key] = arg_value
            self._add_pyinstaller_args()
            self._set_subprocess_working_dir()

    def _add_pyinstaller_args(self) -> None:
        """
        将命令参数字典中的参数按顺序添加到命令参数列表中 \n
        """

        self._args = []  # 避免重复添加

        self._args.append(self.args_dict[PyinstallerArgs.script_path])
        if self.args_dict[PyinstallerArgs.icon_path]:
            self._args.extend(["--icon", self.args_dict[PyinstallerArgs.icon_path]])
        if self.args_dict[PyinstallerArgs.FD]:
            self._args.append(self.args_dict[PyinstallerArgs.FD])
        if self.args_dict[PyinstallerArgs.console]:
            self._args.append(self.args_dict[PyinstallerArgs.console])
        if self.args_dict[PyinstallerArgs.out_name]:
            self._args.extend(["--name", self.args_dict[PyinstallerArgs.out_name]])

        self.args_settled.emit(self._args)

    def _set_subprocess_working_dir(self) -> None:
        """
        设置子进程工作目录 \n
        """

        script_path = self.args_dict[PyinstallerArgs.script_path]
        self._subprocess_working_dir = str(Path(script_path).parent)  # 工作目录设置为脚本所在目录

    def run_packaging_process(self) -> None:
        """
        使用给定的参数启动打包子进程 \n
        """

        self.subprocess.set_working_dir(self._subprocess_working_dir)
        self.subprocess.set_arguments(self._args)
        self.subprocess.start_process(time_out=500)
