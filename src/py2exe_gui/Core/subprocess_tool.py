# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块包含辅助 QProcess 使用的工具类 `SubProcessTool`

待考量：是否有必要使用此类，还是仅需使用其他技巧创建单例QProcess、自行处理信号
"""

__all__ = ["SubProcessTool"]

from enum import IntEnum
from pathlib import Path
from typing import Optional, Sequence, Union
from warnings import warn

from PySide6.QtCore import QIODeviceBase, QObject, QProcess, Signal

from ..Utilities.open_qfile import qba_to_str


class SubProcessTool(QObject):
    """辅助 QProcess 使用的工具类，将所有直接对子进程进行的操作都封装在此类中"""

    # 自定义信号，类型为 tuple[SubProcessTool.OutputType, str]
    output = Signal(tuple)

    # output_types
    class OutputType(IntEnum):
        """枚举值：输出类型"""

        STATE = 1
        STDOUT = 2
        STDERR = 3
        STARTED = 4
        FINISHED = 5
        ERROR = 6

    def __init__(
        self,
        program: str,
        *,
        parent: Optional[QObject] = None,
        arguments: Sequence[str] = (),
        working_directory: str = "./",
    ) -> None:
        """
        :param parent: 父对象
        :param program: 待运行的子进程
        :param arguments: 运行参数
        :param working_directory: 子进程工作目录
        """

        super().__init__(parent)

        self.program: str = program
        self._arguments: Sequence[str] = arguments
        self._working_directory: str = working_directory
        self._process: Optional[QProcess] = None
        self.exit_code: int = 0
        self.exit_status: QProcess.ExitStatus = QProcess.ExitStatus.NormalExit

    def _connect_signals(self) -> None:
        """连接信号"""

        self._process.stateChanged.connect(self._handle_state)  # type: ignore
        self._process.readyReadStandardOutput.connect(self._handle_stdout)  # type: ignore
        self._process.readyReadStandardError.connect(self._handle_stderr)  # type: ignore
        self._process.started.connect(self._process_started)  # type: ignore
        self._process.finished.connect(self._process_finished)  # type: ignore
        self._process.errorOccurred.connect(self._handle_error)  # type: ignore

    def start_process(
        self,
        *,
        mode: QIODeviceBase.OpenModeFlag = QIODeviceBase.OpenModeFlag.ReadWrite,
        time_out: int = 1000,
    ) -> bool:
        """创建并启动子进程，有阻塞

        :param mode: 设备打开的模式
        :param time_out: 启动进程超时时间（单位为毫秒）
        :return: 是否成功启动
        """

        if self._process is None:  # 防止在子进程运行结束前重复启动
            self._process = QProcess(self)
            self._connect_signals()
            self._process.setWorkingDirectory(self._working_directory)
            self._process.start(self.program, self._arguments, mode)
            return self._process.waitForStarted(time_out)  # 阻塞，直到成功启动子进程或超时
        return False

    def abort_process(self, timeout: int = 5000) -> bool:
        """尝试中止子进程，超时后杀死子进程。若子进程没有运行，则什么都不做。

        :param timeout: 超时时间，单位为毫秒
        :return: 子进程是否已结束
        """

        if self._process:
            self._process.terminate()
            is_finished = self._process.waitForFinished(timeout)  # 阻塞，直到进程终止或超时
            if not is_finished:
                self._process.kill()  # 超时后杀死子进程
            return is_finished
        else:
            # 如果子进程没有运行，则认为已结束
            return True

    def set_program(self, program: str) -> None:
        """设置子进程程序

        :param program: 程序名称
        """

        self.program = program

    def set_arguments(self, arguments: Sequence[str]) -> None:
        """设置子进程参数

        :param arguments: 参数列表
        """

        self._arguments = arguments

    def set_working_dir(self, work_dir: Union[str, Path]) -> bool:
        """设置子进程工作目录

        :param work_dir: 工作目录
        :return: 是否设置成功
        """

        working_dir = Path(work_dir)
        if working_dir.is_dir():
            self._working_directory = str(working_dir.absolute())
            return True
        else:
            return False

    def _process_started(self) -> None:
        """处理子进程开始的槽"""

        self.output.emit((self.OutputType.STARTED, "started"))

    def _process_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """处理子进程结束的槽

        :param code: 退出码
        :param status: 退出状态
        """

        self.exit_code = code
        self.exit_status = status
        self.output.emit((self.OutputType.FINISHED, str(code)))
        self._process = None

    def _handle_stdout(self) -> None:
        """处理标准输出的槽"""

        if self._process:
            data = self._process.readAllStandardOutput()
            stdout = qba_to_str(data)
            self.output.emit((self.OutputType.STDOUT, stdout))

    def _handle_stderr(self) -> None:
        """处理标准错误的槽"""

        if self._process:
            data = self._process.readAllStandardError()
            stderr = qba_to_str(data)
            self.output.emit((self.OutputType.STDERR, stderr))

    def _handle_state(self, state: QProcess.ProcessState) -> None:
        """将子进程运行状态转换为易读形式

        :param state: 进程运行状态
        """

        states = {
            QProcess.ProcessState.NotRunning: "The process is not running.",
            QProcess.ProcessState.Starting: "The process is starting...",
            QProcess.ProcessState.Running: "The process is running...",
        }
        state_name = states[state]
        self.output.emit((self.OutputType.STATE, state_name))

    def _handle_error(self, error: QProcess.ProcessError) -> None:
        """处理子进程错误

        :param error: 子进程错误类型
        """

        process_error = {
            QProcess.ProcessError.FailedToStart: "The process failed to start.",
            QProcess.ProcessError.Crashed: "The process has crashed.",
            QProcess.ProcessError.Timedout: "The process has timed out.",
            QProcess.ProcessError.WriteError: "A write error occurred in the process.",
            QProcess.ProcessError.ReadError: "A read error occurred in the process",
            QProcess.ProcessError.UnknownError: "An unknown error has occurred in the process.",
        }
        error_type = process_error[error]

        if self._process:
            self.abort_process(0)
        self.output.emit((self.OutputType.ERROR, error_type))
        warn(error_type, category=RuntimeWarning, stacklevel=3)
        self._process = None
