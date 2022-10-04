from pathlib import Path
from typing import Optional

from PySide6 import QtCore

from .validators import FilePathValidator, InterpreterValidator


class PackagingTask(QtCore.QObject):
    """
    打包任务类，存储每个打包任务的详细信息
    """

    # 自定义信号
    option_set = QtCore.Signal(tuple)  # 用户输入选项通过了验证，已设置为打包选项
    option_error = QtCore.Signal()  # 用户输入选项有误，需要进一步处理

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(PackagingTask, self).__init__(parent)

        self.script_path: Optional[Path] = None
        self.icon_path: Optional[Path] = None

    def handle_option(self, option: tuple):
        """
        处理用户在界面选择的打包选项 \n
        :param option: 选项
        """

        arg_key, arg_value = option

        # 进行有效性验证，有效则保存并发射option_set信号，无效则发射option_error信号
        if arg_key == "script_path":
            self.option_set.emit(option)
        elif arg_key == "icon_path":
            self.option_set.emit(option)
        elif arg_key == "FD":
            self.option_set.emit(option)
        elif arg_key == "console":
            self.option_set.emit(option)
        elif arg_key == "out_name":
            self.option_set.emit(option)

    def write_to_file(self):
        """
        将打包任务保存至文件
        """

        pass
