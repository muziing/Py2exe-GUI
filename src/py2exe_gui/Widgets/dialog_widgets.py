# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块集中处理数个对话框(QDialog)控件
"""

__all__ = [
    "ScriptFileDlg",
    "IconFileDlg",
    "InterpreterFileDlg",
    "AboutDlg",
    "PkgBrowserDlg",
]

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

from ..Constants import RUNTIME_INFO, Platform
from ..Utilities import QObjTr, QtFileOpen


class ScriptFileDlg(QObjTr, QFileDialog):
    """用于获取入口脚本文件的对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setNameFilters(
            (
                ScriptFileDlg.tr("Python Script (*.py *.pyw)"),
                ScriptFileDlg.tr("All Files (*)"),
            )
        )
        self.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.setLabelText(
            QFileDialog.DialogLabel.FileName, ScriptFileDlg.tr("Python Entry File")
        )
        self.setLabelText(
            QFileDialog.DialogLabel.FileType, ScriptFileDlg.tr("Python File")
        )
        self.setLabelText(QFileDialog.DialogLabel.Accept, ScriptFileDlg.tr("Open"))
        self.setLabelText(QFileDialog.DialogLabel.Reject, ScriptFileDlg.tr("Cancel"))


class IconFileDlg(QObjTr, QFileDialog):
    """用于获取应用图标文件的对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setNameFilters(
            (
                IconFileDlg.tr("Icon Files (*.ico *.icns)"),
                IconFileDlg.tr("All Files (*)"),
            )
        )
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.FileName, IconFileDlg.tr("App Icon"))
        self.setLabelText(QFileDialog.DialogLabel.FileType, IconFileDlg.tr("Icon File"))
        self.setLabelText(QFileDialog.DialogLabel.Accept, IconFileDlg.tr("Open"))
        self.setLabelText(QFileDialog.DialogLabel.Reject, IconFileDlg.tr("Cancel"))


class InterpreterFileDlg(QObjTr, QFileDialog):
    """用于获取 Python 解释器可执行文件的对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(
            QFileDialog.DialogLabel.FileName,
            InterpreterFileDlg.tr("Python Interpreter"),
        )
        self.setLabelText(
            QFileDialog.DialogLabel.FileType, InterpreterFileDlg.tr("Executable File")
        )

        if RUNTIME_INFO.platform == Platform.windows:
            self.setNameFilters(
                (
                    InterpreterFileDlg.tr("Python Interpreter (python.exe)"),
                    InterpreterFileDlg.tr("Executable Files (*.exe)"),
                    InterpreterFileDlg.tr("All Files (*)"),
                )
            )
        else:
            self.setNameFilters(
                (
                    InterpreterFileDlg.tr("Python Interpreter (python3*)"),
                    InterpreterFileDlg.tr("All Files (*)"),
                )
            )


class AboutDlg(QObjTr, QMessageBox):
    """用于显示关于信息的对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self._about_text: str = ""
        self.setWindowTitle(AboutDlg.tr("About"))
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setText(self.about_text)
        self.setIconPixmap(QPixmap(":/Icons/Py2exe-GUI_icon_72px"))

    @property
    def about_text(self) -> str:
        """返回本程序的关于信息文本

        :return: 关于信息
        """

        try:
            # 因使用qrc/rcc系统，所以使用Qt风格读取文本文件
            with QtFileOpen(":/Texts/About_Text", encoding="utf-8") as about_file:
                self._about_text = about_file.read()
        except OSError as e:
            warnings.warn(
                f"Cannot open About document: {e}", RuntimeWarning, stacklevel=1
            )
            self._about_text = AboutDlg.tr(
                "Can't open the About document, try to reinstall this program."
            )

        return self._about_text


class PkgBrowserDlg(QObjTr, QDialog):
    """浏览已安装的所有包的对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.pkg_list: list[tuple[str, str]] = []  # [("black", "23.12.1"), ...]
        self.pkg_table = QTableWidget(self)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """处理 UI"""

        self.setWindowTitle(PkgBrowserDlg.tr("Installed Packages"))
        self.setWindowIcon(QIcon(QPixmap(":/Icons/Python_128px")))

        self.pkg_table.setColumnCount(2)
        self.pkg_table.setHorizontalHeaderLabels(
            [PkgBrowserDlg.tr("Name"), PkgBrowserDlg.tr("Version")]
        )
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
        """从后端加载包数据，存储到实例属性 pkg_list 中，并更新界面

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
        """更新包列表控件显示内容"""

        self.pkg_table.setRowCount(len(self.pkg_list))
        for row, pkg in enumerate(self.pkg_list):
            self.pkg_table.setItem(row, 0, QTableWidgetItem(pkg[0]))
            self.pkg_table.setItem(row, 1, QTableWidgetItem(pkg[1]))
