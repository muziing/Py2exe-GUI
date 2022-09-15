from typing import List, Optional

from PySide6 import QtCore
from PySide6.QtCore import QObject

from .subprocess_tool import SubProcessTool


class Packaging(QObject):
    """执行打包的类"""

    # 自定义信号
    args_settled = QtCore.Signal(list)

    def __init__(self, parent: Optional[QObject] = None):
        super(Packaging, self).__init__(parent)
        pyinstaller_args: list = [
            "script_path",
            "icon_path",
            "FD",
            "console",
            "out_name",
        ]
        self.args_dict: dict = dict.fromkeys(pyinstaller_args, "")
        self._args: List[str] = []
        self._subprocess: SubProcessTool = SubProcessTool(self)

    def set_pyinstaller_args(self, arg: tuple[str, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并添加至命令参数字典 \n
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if arg_key in self.args_dict.keys():
            self.args_dict[arg_key] = arg_value
        self._add_pyinstaller_args()

    def _add_pyinstaller_args(self) -> None:
        """
        将命令参数字典中的参数按顺序添加到命令参数列表中 \n
        :return: None
        """

        self._args = []  # 避免重复添加
        self._args.extend([self.args_dict["script_path"]])
        if self.args_dict["icon_path"]:
            self._args.extend(["--icon", self.args_dict["icon_path"]])
        if self.args_dict["FD"]:
            if self.args_dict["FD"] == "One Dir":
                self._args.extend(["--onedir"])
            elif self.args_dict["FD"] == "One File":
                self._args.extend(["--onefile"])
        if self.args_dict["console"]:
            if self.args_dict["console"] == "console":
                self._args.extend(["--console"])
            elif self.args_dict["console"] == "windowed":
                self._args.extend(["--windowed"])
        if self.args_dict["out_name"]:
            self._args.extend(["--name", self.args_dict["out_name"]])

        self.args_settled.emit(self._args)

    def run_packaging_process(self) -> None:
        """
        使用给定的参数启动打包子进程 \n
        :return: None
        """

        # self._subprocess.output.connect(lambda val: print(val))  # 测试用
        self._subprocess.start_process("pyinstaller", self._args)

    def abort_process(self) -> int:
        """
        紧急终止打包进程 \n
        :return: 子进程返回值
        """

        if self._subprocess.process:
            result = 0

            def handel(output: tuple):
                """处理子进程的输出，获取进程结束的返回值"""
                nonlocal result
                if output[0] == 1:
                    result = int(output[1])

            self._subprocess.output.connect(handel)
            self._subprocess.process.terminate()
            self._subprocess.process.waitForFinished(10000)
            return result
        else:
            return 0
