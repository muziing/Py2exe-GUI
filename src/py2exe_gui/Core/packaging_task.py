# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from pathlib import Path
from typing import Optional

from PySide6 import QtCore

from ..Constants import PyinstallerArgs
from .validators import FilePathValidator


class PackagingTask(QtCore.QObject):
    """
    打包任务类，存储每个打包任务的详细信息 \n
    """

    # 自定义信号
    option_set = QtCore.Signal(tuple)  # 用户输入选项通过了验证，已设置为打包选项
    option_error = QtCore.Signal(str)  # 用户输入选项有误，需要进一步处理
    ready_to_pack = QtCore.Signal(bool)  # 是否已经可以运行该打包任务

    def __init__(self, parent: Optional[QtCore.QObject] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(PackagingTask, self).__init__(parent)

        self.script_path: Optional[Path] = None
        self.icon_path: Optional[Path] = None
        self.out_name: Optional[str] = None
        self.FD: Optional[bool] = None
        self.console: Optional[str] = None

    def handle_option(self, option: tuple[PyinstallerArgs, str]):
        """
        处理用户在界面选择的打包选项，进行有效性验证并保存 \n
        :param option: 选项
        """

        arg_key, arg_value = option

        # 进行有效性验证，有效则保存并发射option_set信号，无效则发射option_error信号
        if arg_key == PyinstallerArgs.script_path:
            script_path = Path(arg_value)
            if FilePathValidator.validate_script(script_path):
                self.script_path = script_path
                self.ready_to_pack.emit(True)
                self.option_set.emit(option)
                self.out_name = script_path.stem  # 输出名默认与脚本名相同
                self.option_set.emit((PyinstallerArgs.out_name, self.out_name))
            else:
                self.ready_to_pack.emit(False)
                self.option_error.emit(arg_key)

        elif arg_key == PyinstallerArgs.icon_path:
            icon_path = Path(arg_value)
            if FilePathValidator.validate_icon(icon_path):
                self.icon_path = icon_path
                self.option_set.emit(option)
            else:
                self.option_error.emit(arg_key)

        elif arg_key == PyinstallerArgs.out_name:
            self.out_name = arg_value
            self.option_set.emit(option)

        else:
            self.option_set.emit(option)

    def write_to_spec(self):
        """
        将打包任务保存至spec文件 \n
        """

        pass
