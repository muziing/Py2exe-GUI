from pathlib import Path
from typing import Optional

from PySide6 import QtCore

from .validators import FilePathValidator


class PackagingTask(QtCore.QObject):
    """
    打包任务类，存储每个打包任务的详细信息
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
        # TODO 在实例属性中保存该次打包的所有选项详情

    def handle_option(self, option: tuple[str, str]):
        """
        处理用户在界面选择的打包选项，进行有效性验证并保存 \n
        :param option: 选项
        """

        arg_key, arg_value = option

        # 进行有效性验证，有效则保存并发射option_set信号，无效则发射option_error信号
        if arg_key == "script_path":
            script_path = Path(arg_value)
            if FilePathValidator.validate_script(script_path):
                self.script_path = script_path
                self.ready_to_pack.emit(True)
                self.option_set.emit(option)
                self.out_name = script_path.stem  # 输出名默认与脚本名相同
                self.option_set.emit(("out_name", self.out_name))
            else:
                self.ready_to_pack.emit(False)
                self.option_error.emit(arg_key)
            # self.option_error.emit(arg_key)  # 测试用！

        elif arg_key == "icon_path":
            icon_path = Path(arg_value)
            if FilePathValidator.validate_icon(icon_path):
                self.icon_path = icon_path
                self.option_set.emit(option)
            else:
                self.option_error.emit(arg_key)
            # self.option_error.emit(arg_key)  # 测试用！

        elif arg_key == "out_name":
            self.out_name = arg_value
            self.option_set.emit(option)

        else:
            self.option_set.emit(option)

    def write_to_file(self):
        """
        将打包任务保存至文件
        """

        # TODO 实现将打包任务信息保存至文件的功能
        pass
