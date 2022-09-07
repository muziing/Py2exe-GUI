from sys import getdefaultencoding
from typing import Optional, Sequence

from PySide6 import QtCore


class QSubProcessTool(QtCore.QObject):
    """辅助使用QProcess创建并管理子进程的工具类"""

    # 自定义信号，参数为 (output_type: QSubProcessTool.output_type, output_text: str)
    output = QtCore.Signal(tuple)

    # output_types
    STATE = 0
    FINISHED = 1
    STDOUT = 2
    STDERR = 3

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        super(QSubProcessTool, self).__init__(parent)
        self.process: Optional[QtCore.QProcess] = None

    def start_process(self, program: str, arguments: Sequence[str]) -> None:
        """
        使用给定参数启动指定子进程 \n
        :param program: 子进程命令
        :param arguments: 子进程参数
        :return: None
        """

        if self.process is None:  # 防止在子进程运行结束前重复启动
            self.process = QtCore.QProcess()

            self.process.stateChanged.connect(self._handle_state)  # type: ignore
            self.process.readyReadStandardOutput.connect(self._handle_stdout)  # type: ignore
            self.process.readyReadStandardError.connect(self._handle_stderr)  # type: ignore
            self.process.started.connect(self._process_started)  # type: ignore
            self.process.finished.connect(self._process_finished)  # type: ignore

            self.process.start(program, arguments)

    def _process_started(self) -> None:
        """
        处理子进程的槽 \n
        :return: None
        """
        pass

    def _process_finished(self) -> None:
        """
        处理子进程的槽 \n
        :return: None
        """

        self.output.emit((self.FINISHED, "Subprocess finished."))
        self.process = None

    def _handle_stdout(self) -> None:
        """
        处理标准输出的槽 \n
        :return: None
        """

        if self.process:
            data = self.process.readAllStandardOutput()
            stdout = bytes(data).decode(getdefaultencoding())
            self.output.emit((self.STDOUT, stdout))

    def _handle_stderr(self) -> None:
        """
        处理标准错误的槽 \n
        :return: None
        """

        if self.process:
            data = self.process.readAllStandardError()
            stderr = bytes(data).decode(getdefaultencoding())
            self.output.emit((self.STDERR, stderr))

    def _handle_state(self, state: QtCore.QProcess.ProcessState) -> None:
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
        self.output.emit((self.STATE, state_name))
