# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import warnings
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHeaderView,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..Utilities import QtFileOpen


class ScriptFileDlg(QFileDialog):
    """
    用于获取入口脚本文件的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setNameFilters(("Python脚本文件 (*.py *.pyw)", "所有文件 (*)"))
        self.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.setLabelText(QFileDialog.DialogLabel.FileName, "Python入口文件")
        self.setLabelText(QFileDialog.DialogLabel.FileType, "Python文件")
        self.setLabelText(QFileDialog.DialogLabel.Accept, "打开")
        self.setLabelText(QFileDialog.DialogLabel.Reject, "取消")


class IconFileDlg(QFileDialog):
    """
    用于获取应用图标文件的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setNameFilters(("图标文件 (*.ico *.icns)", "所有文件 (*)"))
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.FileName, "图标")
        self.setLabelText(QFileDialog.DialogLabel.FileType, "图标文件")
        self.setLabelText(QFileDialog.DialogLabel.Accept, "打开")
        self.setLabelText(QFileDialog.DialogLabel.Reject, "取消")


class AboutDlg(QMessageBox):
    """
    用于显示关于信息的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self._about_text: str = ""
        self.setWindowTitle("关于")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setText(self.about_text)
        self.setIconPixmap(QPixmap(":/Icons/Py2exe-GUI_icon_72px"))

    @property
    def about_text(self) -> str:
        """
        返回本程序的关于信息文本 \n
        :return: 关于信息
        """

        try:
            # 因使用qrc/rcc系统，所以使用Qt风格读取文本文件
            with QtFileOpen(":/Texts/About_Text", encoding="utf-8") as about_file:
                self._about_text = about_file.read()
        except OSError as e:
            warnings.warn(f"无法打开关于文档，错误信息：{e}", RuntimeWarning, stacklevel=1)
            self._about_text = "无法打开关于文档，请尝试重新获取本程序。"

        return self._about_text


class PkgBrowserDlg(QDialog):
    """
    浏览已安装的所有包的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.pkg_list: list[tuple[str, str]] = []  # [("black", "23.12.1"), ...]
        self.pkg_table = QTableWidget(self)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        处理 UI \n
        """

        self.setWindowTitle("已安装的包")
        self.setWindowIcon(QIcon(QPixmap(":/Icons/Python_128px")))

        self.pkg_table.setColumnCount(2)
        self.pkg_table.setHorizontalHeaderLabels(["包名", "版本"])
        self.pkg_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.pkg_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.pkg_table)
        self.setLayout(main_layout)

    def load_pkg_list(self, pkg_list: list[dict[str, str]]) -> None:
        """
        从后端加载包数据，存储到实例属性 pkg_list 中 \n
        self.pkg_list 形如 [("black", "23.12.1"), ...]
        :param pkg_list: 已安装的包列表，形如 [{"name": "black", "version": "23.12.1"}, {}, ...]
        """

        package_lists = []
        for pkg in pkg_list:
            pkg_name = pkg["name"]
            pkg_version = pkg["version"]
            package_lists.append((pkg_name, pkg_version))
        self.pkg_list = package_lists
        self._pkg_table_update()

    def _pkg_table_update(self) -> None:
        """
        更新包列表控件显示内容 \n
        """

        self.pkg_table.setRowCount(len(self.pkg_list))
        for row, pkg in enumerate(self.pkg_list):
            self.pkg_table.setItem(row, 0, QTableWidgetItem(pkg[0]))
            self.pkg_table.setItem(row, 1, QTableWidgetItem(pkg[1]))
