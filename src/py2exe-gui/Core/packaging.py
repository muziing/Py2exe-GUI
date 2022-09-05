import subprocess
from typing import List

from PySide6.QtCore import QProcess


class Packaging:
    """执行打包的核心"""

    def __init__(self):
        pyinstaller_args: list = ["script_path", "icon_path", "FD", "console"]
        self.args_dict: dict = dict.fromkeys(pyinstaller_args, "")
        self._args: List[str] = []
        self.p = None

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
        full_args = self.args_dict
        self._args.extend([full_args["script_path"]])
        if full_args["icon_path"]:
            self._args.extend(["--icon", full_args["icon_path"]])
        if full_args["FD"]:
            if full_args["FD"] == "One Dir":
                self._args.extend(["--onedir"])
            elif full_args["FD"] == "One File":
                self._args.extend(["--onefile"])
        if full_args["console"]:
            if full_args["console"] == "console":
                self._args.extend(["--console"])
            elif full_args["console"] == "windowed":
                self._args.extend(["--windowed"])

        print(self._args)  # 测试用

    def run_packaging_process(self) -> None:
        """
        使用给定的参数启动打包子进程 \n
        :return: None
        """

        self.p = QSubProcessTool()
        self.p.start_process("pyinstaller", self._args)


class QSubProcessTool:
    """自定义的辅助使用QProcess子进程的类"""

    def __init__(self):
        self.process = None

    def start_process(self, program, arguments):
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)  # type: ignore
            self.process.stateChanged.connect(self.handle_state)  # type: ignore
            self.process.finished.connect(self.process_finished)  # type: ignore
            self.process.start(program, arguments)

    def process_finished(self):
        print("Subprocess finished.")
        self.process = None

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")


if __name__ == "__main__":
    packager = Packaging()
    packager._args += ["-v"]
    print(packager.run_packaging_process())
