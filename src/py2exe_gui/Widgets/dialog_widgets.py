# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from typing import Optional

from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget


class ScriptFileDlg(QFileDialog):
    """
    用于获取入口脚本文件的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self._setup()

    def _setup(self) -> None:
        """
        配置脚本路径对话框 \n
        """

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

        self._setup()

    def _setup(self) -> None:
        """
        配置应用图标对话框 \n
        """

        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setNameFilters(("图标文件 (*.ico *.icns)", "所有文件 (*)"))
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setLabelText(QFileDialog.DialogLabel.FileName, "图标")
        self.setLabelText(QFileDialog.DialogLabel.FileType, "图标文件")
        self.setLabelText(QFileDialog.DialogLabel.Accept, "打开")
        self.setLabelText(QFileDialog.DialogLabel.Reject, "取消")


class AddDataDlg(QFileDialog):
    """
    用于添加附加数据的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self._setup()

    def _setup(self) -> None:
        """
        配置添加数据对话框 \n
        """

        pass


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
        self._setup()

    def _setup(self) -> None:
        """
        配置关于信息对话框 \n
        """

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

        # 因使用qrc/rcc系统，所以使用Qt风格读取文本文件
        about_file = QFile(":/Texts/About_Text")
        about_file.open(QIODevice.ReadOnly | QIODevice.Text)  # type: ignore
        about_text = str(about_file.readAll(), encoding="utf-8")  # type: ignore
        about_file.close()

        if about_text:
            self._about_text = about_text
        else:
            self._about_text = "无法打开关于文档，请尝试重新获取本程序。"

        return self._about_text
