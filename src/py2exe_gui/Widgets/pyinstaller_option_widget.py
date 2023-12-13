# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import warnings

import yaml
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from ..Constants import RUNTIME_INFO


def get_options() -> list[dict]:
    """
    从数据文件中读取并解析 PyInstaller 命令选项信息，按运行时平台筛选后返回 \n
    :return: 选项信息字典列表
    """

    option_file = QFile(":/Texts/PyInstaller_Options")
    option_file.open(QIODevice.ReadOnly | QIODevice.Text)  # type: ignore
    option_file_text = str(option_file.readAll(), encoding="utf-8")  # type: ignore
    option_file.close()

    if option_file_text == "":
        warnings.warn("PyInstaller_Options 加载失败，检查资源文件", Warning, stacklevel=1)
        return []

    data = yaml.load(option_file_text, Loader=yaml.Loader)

    def filter_option(option) -> bool:
        # 根据当前运行的平台，筛选有效的 PyInstaller 选项
        return (
            option["platform"] == ["all"]
            or RUNTIME_INFO.platform.value in option["platform"]
        )

    current_options = [option for option in data["options"] if filter_option(option)]

    return current_options


class PyinstallerOptionTable(QTableWidget):
    """
    用于显示 PyInstaller 命令行选项的表格控件
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PyInstaller 命令选项")
        self.setMinimumSize(650, 430)
        self.setWindowIcon(QPixmap(":/Icons/PyInstaller"))

        self.option_list = get_options()

        self.setRowCount(len(self.option_list))
        self.setColumnCount(2)
        self.set_items()
        self.setHorizontalHeaderLabels(["选项", "描述"])
        # 将第二列的宽度设置为自动调整
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def set_items(self) -> None:
        """
        为表格控件中填充条目
        """

        for index, option in enumerate(self.option_list):
            self.setItem(index, 0, QTableWidgetItem(option["option"]))
            self.setItem(index, 1, QTableWidgetItem(option["description"]))
