from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMessageBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from py2exe_gui.Core.subprocess_tool import SubProcessTool


class ScriptFileDlg(QFileDialog):
    """
    用于获取入口脚本文件的对话框
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(ScriptFileDlg, self).__init__(parent)

        self._setup()

    def _setup(self) -> None:
        """
        配置脚本路径对话框 \n
        """

        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setViewMode(QFileDialog.Detail)
        self.setNameFilters(("Python脚本文件 (*.py *.pyw)", "所有文件 (*)"))
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setLabelText(QFileDialog.FileName, "Python入口文件")
        self.setLabelText(QFileDialog.FileType, "Python文件")
        self.setLabelText(QFileDialog.Accept, "打开")
        self.setLabelText(QFileDialog.Reject, "取消")


class IconFileDlg(QFileDialog):
    """
    用于获取应用图标文件的对话框
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(IconFileDlg, self).__init__(parent)

        self._setup()

    def _setup(self) -> None:
        """
        配置应用图标对话框 \n
        """

        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setViewMode(QFileDialog.Detail)
        self.setNameFilters(("图标文件 (*.ico *.icns)", "所有文件 (*)"))
        self.setFileMode(QFileDialog.ExistingFile)
        self.setLabelText(QFileDialog.FileName, "图标")
        self.setLabelText(QFileDialog.FileType, "图标文件")
        self.setLabelText(QFileDialog.Accept, "打开")
        self.setLabelText(QFileDialog.Reject, "取消")


class AddDataDlg(QFileDialog):
    """
    用于添加附加数据的对话框
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(AddDataDlg, self).__init__(parent)

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

    def __init__(self, parent: QWidget = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(AboutDlg, self).__init__(parent)

        self._about_text: str = ""
        self._setup()

    def _setup(self) -> None:
        """
        配置关于信息对话框 \n
        """

        self.setWindowTitle("关于")
        self.setStandardButtons(QMessageBox.Ok)
        self.setTextFormat(Qt.MarkdownText)
        self.setText(self.about_text)
        self.setIconPixmap(
            QPixmap("py2exe_gui/Resources/Icons/Py2exe-GUI_icon_72px.png")
        )

    @property
    def about_text(self) -> str:
        """
        返回本程序的关于信息文本 \n
        :return: 关于信息
        """

        try:
            with open(
                "py2exe_gui/Resources/About.md", "r", encoding="utf-8"
            ) as about_file:
                self._about_text = about_file.read()
        except FileNotFoundError:
            self._about_text = "无法打开关于文档，请尝试重新获取本程序。"

        return self._about_text


class SubProcessDlg(QDialog):
    """
    用于显示子进程信息的对话框
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(SubProcessDlg, self).__init__(parent)

        self.info_label = QLabel(self)
        self.browser = QTextBrowser(self)
        self._setup()

    def _setup(self) -> None:
        """
        配置子进程信息对话框 \n
        """

        self.setWindowTitle("PyInstaller")
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def handle_output(self, subprocess_output: tuple[int, str]) -> None:
        """
        处理子进程的输出 \n
        :param subprocess_output: 子进程输出
        """

        output_type, output_text = subprocess_output
        if output_type == SubProcessTool.STDOUT:
            self.browser.append(output_text)
        elif output_type == SubProcessTool.STDERR:
            self.browser.append(output_text)
        elif output_type == SubProcessTool.FINISHED:
            self.info_label.setText("打包完成！")
        elif output_type == SubProcessTool.STATE:
            self.info_label.setText(output_text)


if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # window = ScriptFileDlg()
    # window = IconFileDlg()
    # window.fileSelected.connect(lambda f: print(f))  # type: ignore
    # window = AboutDlg()
    window = SubProcessDlg()
    window.open()
    sys.exit(app.exec())
