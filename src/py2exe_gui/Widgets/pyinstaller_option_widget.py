# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""本模块主要用于加载、解析、界面显示 PyInstaller 选项的详细描述

`load_pyinst_options()` 函数用于从数据文件中读取并解析 PyInstaller 命令选项信息，按运行时平台筛选后返回；
`PyinstallerOptionTable` 类是用于显示 PyInstaller 命令行选项的表格控件窗口，界面有待进一步优化
"""

__all__ = [
    "load_pyinst_options",
    "PyinstallerOptionTable",
]

import warnings

import yaml
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from ..Constants import RUNTIME_INFO
from ..Utilities import QObjTr, QtFileOpen


def load_pyinst_options() -> dict[str, str]:
    """从数据文件中读取并解析 PyInstaller 命令选项信息，按运行时平台筛选后返回

    若加载失败，则抛出警告、返回空字典
    由于涉及QRC资源文件读取与遍历，耗时稍长，应尽量减少此函数调用次数

    :return: 选项信息字典，{option: description}
    """

    try:
        with QtFileOpen(":/Texts/PyInstaller_Options", encoding="utf-8") as option_file:
            option_file_text = option_file.read()
    except OSError as e:
        warnings.warn(
            f"Failed to load PyInstaller Options: {e}", RuntimeWarning, stacklevel=1
        )
        return dict()

    try:
        # 优先使用性能更高的 CLoader 进行解析
        opt_data = yaml.load(option_file_text, Loader=yaml.CLoader)
    except AttributeError:
        # 如果没有可用的 C 扩展，则使用纯 Python 解析
        # https://pyyaml.org/wiki/PyYAMLDocumentation
        opt_data = yaml.load(option_file_text, Loader=yaml.Loader)

    option_dict = {
        option["option"]: option["description"]
        for option in opt_data["options"]
        if (
            option["platform"] == ["all"]
            or RUNTIME_INFO.platform.value in option["platform"]
        )
    }

    return option_dict


class PyinstallerOptionTable(QObjTr, QTableWidget):
    """用于显示 PyInstaller 命令行选项的表格控件"""

    def __init__(self) -> None:
        super().__init__()

        # 设置界面
        self.setWindowTitle("PyInstaller 命令选项")
        self.setMinimumSize(700, 430)
        self.setWindowIcon(QPixmap(":/Icons/PyInstaller"))
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(
            [
                PyinstallerOptionTable.tr("Option"),
                PyinstallerOptionTable.tr("Description"),
            ]
        )
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # 存储选项信息的字典
        self.option_dict = load_pyinst_options()
        self._set_option_items()

    def _set_option_items(self) -> None:
        """加载选项信息、为表格控件中填充条目"""

        # 填充条目
        self.setRowCount(len(self.option_dict))
        for index, (option, description) in enumerate(self.option_dict.items()):
            self.setItem(index, 0, QTableWidgetItem(option))
            self.setItem(index, 1, QTableWidgetItem(description))
