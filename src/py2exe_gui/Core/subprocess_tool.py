import os.path
from sys import getdefaultencoding
from typing import Optional, Sequence

from PySide6 import QtCore


class SubProcessTool(QtCore.QObject):
    """
    辅助QProcess使用的工具类，将所有直接对子进程进行的操作都封装在此类中
    """

    # 自定义信号，参数为 tuple[output_type: int, output_text: str]
    output = QtCore.Signal(tuple)

    # output_types
    STATE = 1
    STDOUT = 2
    STDERR = 3
    FINISHED = 4

    def __init__(
        self,
        parent: Optional[QtCore.QObject] = None,
        *,
        program: str = "",
        arguments: Sequence[str] = (),
        working_directory: str = "./",
    ) -> None:
        """
        :param parent: 父对象
        :param program: 待运行的子进程
        :param arguments: 运行参数
        :param working_directory: 子进程工作目录
        """

        super(SubProcessTool, self).__init__(parent)

        self.program: str = program
        self._arguments: Sequence[str] = arguments
        self._working_directory: str = working_directory
        self._process: Optional[QtCore.QProcess] = None
        self.exit_code: int = 0
        self.exit_status: QtCore.QProcess.ExitStatus = QtCore.QProcess.NormalExit

    def start_process(
        self,
        *,
        mode: QtCore.QIODeviceBase.OpenMode = QtCore.QIODeviceBase.OpenModeFlag.ReadWrite,  # type: ignore
    ) -> None:
        """
        创建并启动子进程 \n
        :param mode: 设备打开的模式
        """

        if self._process is None:  # 防止在子进程运行结束前重复启动
            self._process = QtCore.QProcess(self)

            self._process.stateChanged.connect(self._handle_state)  # type: ignore
            self._process.readyReadStandardOutput.connect(self._handle_stdout)  # type: ignore
            self._process.readyReadStandardError.connect(self._handle_stderr)  # type: ignore
            self._process.started.connect(self._process_started)  # type: ignore
            self._process.finished.connect(self._process_finished)  # type: ignore
            self._process.errorOccurred.connect(self._handle_error)  # type: ignore

            self._process.setWorkingDirectory(self._working_directory)
            self._process.start(self.program, self._arguments, mode)
            self._process.waitForStarted(1000)  # 阻塞，直到启动了子进程或超时（单位为毫秒）

    def abort_process(self, timeout: int = 10000) -> bool:
        """
        终止子进程 \n
        :param timeout: 超时时间，单位为毫秒
        :return: 子进程是否完成
        """

        if self._process:
            self._process.terminate()
            finished = self._process.waitForFinished(timeout)  # 阻塞，直到进程终止或超时
            if not finished:
                self._process.kill()  # 超时后杀死子进程
            return finished
        else:
            return True

    def set_arguments(self, arguments: Sequence[str]) -> None:
        """
        设置子进程参数 \n
        :param arguments: 参数列表
        """

        self._arguments = arguments

    def set_working_dir(self, work_dir: str) -> bool:
        """
        设置子进程工作目录 \n
        :param work_dir: 工作目录
        :return: 是否设置成功
        """

        if os.path.isdir(work_dir):
            self._working_directory = work_dir
            return True
        else:
            return False

    def _process_started(self) -> None:
        """
        处理子进程开始的槽 \n
        """

        pass

    def _process_finished(self, code: int, status: QtCore.QProcess.ExitStatus) -> None:
        """
        处理子进程结束的槽 \n
        :param code: 退出码
        :param status: 退出状态
        """

        self.exit_code = code
        self.exit_status = status
        self.output.emit((self.FINISHED, str(code)))
        self._process = None

    def _handle_stdout(self) -> None:
        """
        处理标准输出的槽 \n
        """

        if self._process:
            data = self._process.readAllStandardOutput()
            stdout = bytes(data).decode(getdefaultencoding())  # 将QByteArray转为str
            self.output.emit((self.STDOUT, stdout))

    def _handle_stderr(self) -> None:
        """
        处理标准错误的槽 \n
        """

        if self._process:
            data = self._process.readAllStandardError()
            stderr = bytes(data).decode(getdefaultencoding())  # 将QByteArray转为str
            self.output.emit((self.STDERR, stderr))

    def _handle_state(self, state: QtCore.QProcess.ProcessState) -> None:
        """
        将子进程运行状态转换为易读形式 \n
        :param state: 进程运行状态
        """

        states = {
            QtCore.QProcess.NotRunning: "非运行",
            QtCore.QProcess.Starting: "启动中……",
            QtCore.QProcess.Running: "正在运行中……",
        }
        state_name = states[state]
        self.output.emit((self.STATE, state_name))

    def _handle_error(self, error: QtCore.QProcess.ProcessError) -> None:
        """
        处理子进程错误 \n
        :param error: 子进程错误
        """

        pass
