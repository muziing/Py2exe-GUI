# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块主要包含用于呈现 PyInstaller 进程运行状态和输出的控件 `SubProcessDlg`
"""

__all__ = ["SubProcessDlg"]

from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..Core.subprocess_tool import SubProcessTool
from ..Utilities import QObjTr


class SubProcessDlg(QObjTr, QDialog):
    """用于显示子进程信息的对话框"""

    def __init__(self, parent: QWidget) -> None:
        """
        :param parent: 父控件对象，必须为 MainApp 类
        """

        super().__init__(parent)

        self.info_label = QLabel(self)
        self.text_browser = QTextBrowser(self)  # 用于显示子进程输出内容
        self.multifunction_btn = QPushButton(self)  # 可用于“取消”“打开输出位置”等的多功能按钮
        self._setup()

    def _setup(self) -> None:
        """配置子进程信息对话框"""

        self.setWindowTitle("PyInstaller")
        self.setMinimumWidth(500)
        self.setModal(True)

        # 布局管理器
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.text_browser)
        main_layout.addWidget(self.multifunction_btn)
        self.setLayout(main_layout)

    @Slot(tuple)
    def handle_output(
        self, subprocess_output: tuple[SubProcessTool.OutputType, str]
    ) -> None:
        """处理子进程的输出

        :param subprocess_output: 子进程输出，应为二元素元组，第一项为 SubProcessTool.OutputType
        :raise ValueError: 子进程输出的类型不正确
        """

        output_type, output_text = subprocess_output

        if output_type == SubProcessTool.OutputType.STATE:
            self.info_label.setText(output_text)
            if output_text == "The process is running...":
                self.multifunction_btn.setText(SubProcessDlg.tr("Cancel"))

        elif (
            output_type == SubProcessTool.OutputType.STDOUT
            or output_type == SubProcessTool.OutputType.STDERR
        ):
            self.text_browser.append(output_text)

        elif output_type == SubProcessTool.OutputType.FINISHED:
            if output_text == "0":
                self.info_label.setText(SubProcessDlg.tr("Done!"))
                self.multifunction_btn.setText(SubProcessDlg.tr("Open Dist"))
            else:
                self.info_label.setText(
                    SubProcessDlg.tr(
                        "Execution ends, but an error occurs and the exit code is"
                    )
                    + f"{output_text}"
                )
                self.multifunction_btn.setText(SubProcessDlg.tr("Cancel"))

        elif output_type == SubProcessTool.OutputType.ERROR:
            self.info_label.setText(SubProcessDlg.tr("PyInstaller Error!"))
            self.text_browser.append(
                SubProcessDlg.tr("PyInstaller subprocess output:") + f"{output_text}"
            )
            self.text_browser.append(
                SubProcessDlg.tr(
                    "Please check if you have installed "
                    "the correct version of PyInstaller or not."
                )
            )
            self.multifunction_btn.setText(SubProcessDlg.tr("Close"))

        elif not isinstance(output_type, SubProcessTool.OutputType):
            raise ValueError(f"Unsupported output type: {output_type}")

    def closeEvent(self, event: QCloseEvent) -> None:
        """重写关闭事件，进行收尾清理

        :param event: 关闭事件
        """

        # 显式发送一次 finished 信号，外部接收到此信号后应主动中断 PyInstaller 进程
        self.finished.emit(-1)

        self.text_browser.clear()
        super().closeEvent(event)
