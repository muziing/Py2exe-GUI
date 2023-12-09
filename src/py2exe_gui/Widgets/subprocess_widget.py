# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

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


class SubProcessDlg(QDialog):
    """
    用于显示子进程信息的对话框
    """

    def __init__(self, parent: QWidget) -> None:
        """
        :param parent: 父控件对象，必须为 MainApp 类
        """

        super().__init__(parent)

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
        self.setModal(True)  # 设置为模态对话框

        # 布局管理器
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.browser)
        main_layout.addWidget(self.multifunction_btn)
        self.setLayout(main_layout)

    @Slot(tuple)
    def handle_output(self, subprocess_output: tuple[int, str]) -> None:
        """
        处理子进程的输出 \n
        :param subprocess_output: 子进程输出
        """

        output_type, output_text = subprocess_output

        if output_type == SubProcessTool.STATE:
            self.info_label.setText(output_text)
            if output_text == "The process is running...":
                self.multifunction_btn.setText("取消")
        elif (
            output_type == SubProcessTool.STDOUT or output_type == SubProcessTool.STDERR
        ):
            self.browser.append(output_text)
        elif output_type == SubProcessTool.FINISHED:
            if output_text == "0":
                self.info_label.setText("打包完成！")
                self.multifunction_btn.setText("打开输出位置")
            else:
                self.info_label.setText(f"运行结束，但有错误发生，退出码为 {output_text}")
                self.multifunction_btn.setText("取消")
        elif output_type == SubProcessTool.ERROR:
            self.info_label.setText("PyInstaller错误！")
            self.browser.append(f"PyInstaller 子进程输出信息：{output_text}")
            self.browser.append("请检查是否已经安装正确版本的 PyInstaller")
            self.multifunction_btn.setText("关闭")

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        重写关闭事件，进行收尾清理 \n
        :param event: 关闭事件
        """

        self.finished.emit(-1)
        self.browser.clear()
        super().closeEvent(event)
