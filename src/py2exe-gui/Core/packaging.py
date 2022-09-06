from typing import List, Optional, Sequence

from PySide6 import QtCore
from PySide6.QtCore import QObject


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
        self.subprocess: Optional[QSubProcessTool] = None

    def get_pyinstaller_args(self, arg: tuple[str, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并以正确的顺序添加至命令参数字典 \n
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if arg_key in self.args_dict.keys():
            self.args_dict[arg_key] = arg_value
        self.set_pyinstaller_args()

    def set_pyinstaller_args(self) -> None:
        """
        将命令参数字典中的参数按顺序添加到命令参数列表中
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

        self.subprocess = QSubProcessTool()
        self.subprocess.start_process("pyinstaller", self._args)


class QSubProcessTool:
    """自定义的辅助使用QProcess子进程的类"""

    # TODO 将所有输出以信号形式发射
    def __init__(self):
        self.process: Optional[QtCore.QProcess] = None

    def start_process(self, program: str, arguments: Sequence[str]) -> None:
        """
        启动子进程 \n
        :param program: 子进程命令
        :param arguments: 子进程参数
        :return: None
        """

        if self.process is None:  # 防止在子进程运行结束前重复启动
            self.process = QtCore.QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)  # type: ignore
            self.process.readyReadStandardError.connect(self.handle_stderr)  # type: ignore
            self.process.stateChanged.connect(self.handle_state)  # type: ignore
            self.process.finished.connect(self.process_finished)  # type: ignore
            self.process.start(program, arguments)

    def process_finished(self) -> None:
        """
        处理子进程的槽 \n
        :return: None
        """

        print("Subprocess finished.")
        self.process = None

    def handle_stdout(self) -> None:
        """
        处理标准输出的槽 \n
        :return: None
        """

        if self.process:
            data = self.process.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")
            print(stdout)

    def handle_stderr(self) -> None:
        """
        处理标准错误的槽 \n
        :return: None
        """

        if self.process:
            data = self.process.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            print(stderr)

    def handle_state(self, state: QtCore.QProcess.ProcessState) -> None:
        """
        将子进程运行状态转换为易读形式 \n
        :param state: 进程运行状态
        :return: None
        """

        states = {
            QtCore.QProcess.NotRunning: "Not running",
            QtCore.QProcess.Starting: "Starting",
            QtCore.QProcess.Running: "Running",
        }
        state_name = states[state]
        print(f"State changed: {state_name}")
