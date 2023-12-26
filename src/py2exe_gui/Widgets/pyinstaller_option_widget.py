# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import warnings

import yaml
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from ..Constants import RUNTIME_INFO
from ..Utilities import QtFileOpen


def load_pyinst_options() -> dict[str, str]:
    """
    从数据文件中读取并解析 PyInstaller 命令选项信息，按运行时平台筛选后返回 \n
    :return: 选项信息字典，{option: description}
    """

    try:
        with QtFileOpen(":/Texts/PyInstaller_Options", encoding="utf-8") as option_file:
            option_file_text = option_file.read()
    except OSError as e:
        warnings.warn(
            f"PyInstaller Options 加载失败，错误信息：{e}", RuntimeWarning, stacklevel=1
        )
        return dict()

    data = yaml.load(option_file_text, Loader=yaml.Loader)
    option_dict = dict()

    for option in data["options"]:
        if (
            option["platform"] == ["all"]
            or RUNTIME_INFO.platform.value in option["platform"]
        ):
            option_dict.update({option["option"]: option["description"]})

    return option_dict


class PyinstallerOptionTable(QTableWidget):
    """
    用于显示 PyInstaller 命令行选项的表格控件
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PyInstaller 命令选项")
        self.setMinimumSize(700, 430)
        self.setWindowIcon(QPixmap(":/Icons/PyInstaller"))

        self.option_dict = load_pyinst_options()
        self.setRowCount(len(self.option_dict))
        self.setColumnCount(2)
        self._set_items()
        self.setHorizontalHeaderLabels(["选项", "描述"])
        # 将第二列的宽度设置为自动调整
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _set_items(self) -> None:
        """
        为表格控件中填充条目 \n
        """

        for index, (option, description) in enumerate(self.option_dict.items()):
            self.setItem(index, 0, QTableWidgetItem(option))
            self.setItem(index, 1, QTableWidgetItem(description))
