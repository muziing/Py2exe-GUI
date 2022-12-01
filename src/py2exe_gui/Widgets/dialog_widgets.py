import subprocess
from typing import Optional

from PySide6.QtCore import QFile, QIODevice, Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..Core.subprocess_tool import SubProcessTool


class ScriptFileDlg(QFileDialog):
    """
    用于获取入口脚本文件的对话框
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
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

    def __init__(self, parent: Optional[QWidget] = None) -> None:
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

    def __init__(self, parent: Optional[QWidget] = None) -> None:
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

    def __init__(self, parent: Optional[QWidget] = None) -> None:
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
        self.setIconPixmap(QPixmap(":/Icons/Py2exe-GUI_icon_72px"))

    @property
    def about_text(self) -> str:
        """
        返回本程序的关于信息文本 \n
        :return: 关于信息
        """

        # 因使用qrc系统，所以使用Qt风格读取文本文件
        about_file = QFile(":/Texts/About_Text")
        about_file.open(QIODevice.ReadOnly | QIODevice.Text)  # type: ignore
        about_text = bytes(about_file.readAll()).decode("utf-8")
        about_file.close()

        if about_text:
            self._about_text = about_text
        else:
            self._about_text = "无法打开关于文档，请尝试重新获取本程序。"

        return self._about_text


class SubProcessDlg(QDialog):
    """
    用于显示子进程信息的对话框
    """

    def __init__(self, parent: QWidget) -> None:
        """
        :param parent: 父控件对象，必须为 MainApp 类
        """

        super(SubProcessDlg, self).__init__(parent)

        self.info_label = QLabel(self)
        self.browser = QTextBrowser(self)
        self.multifunction_btn = QPushButton(self)  # 可用于“取消”“打开输出位置”等的多功能按钮
        self._setup()

    def _setup(self) -> None:
        """
        配置子进程信息对话框 \n
        """

        self.setWindowTitle("PyInstaller")
        self.setMinimumWidth(400)
        self.setModal(True)

        self.multifunction_btn.setMaximumWidth(80)

        # 布局管理器
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.browser)
        main_layout.addWidget(self.multifunction_btn)
        self.setLayout(main_layout)

        # 连接信号与槽
        self.multifunction_btn.clicked.connect(self.handle_multifunction)  # type:ignore

    @Slot(tuple)
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
            self.multifunction_btn.setText("打开输出位置")
        elif output_type == SubProcessTool.STATE:
            self.info_label.setText(output_text)
            if output_text == "正在运行中……":
                self.multifunction_btn.setText("取消")

    @Slot()
    def handle_multifunction(self) -> None:
        """
        处理多功能按钮点击信号的槽 \n
        """

        btn_text = self.multifunction_btn.text()
        if btn_text == "取消":
            self.parent().packager.subprocess.abort_process()
            self.close()
        elif btn_text == "打开输出位置":
            dist_path = self.parent().packaging_task.script_path.parent / "dist"
            if self.parent().running_platform == "Windows":
                import os  # fmt: skip
                os.startfile(dist_path)  # type: ignore
            elif self.parent().running_platform == "Linux":
                subprocess.call(["xdg-open", dist_path])
            elif self.parent().running_platform == "macOS":
                subprocess.call(["open", dist_path])
