import os
import subprocess
import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

# from .Constants import *
from .Core import Packaging, PackagingTask
from .Widgets import MainWindow, SubProcessDlg


class MainApp(MainWindow):
    """
    主程序
    """

    def __init__(self, *args, **kwargs) -> None:
        super(MainApp, self).__init__(*args, **kwargs)

        self.packaging_task = PackagingTask(self)
        self.packager = Packaging(self)
        self.subprocess_dlg = SubProcessDlg(self)

        self._connect_slots()

        self.status_bar.showMessage("就绪")

    def _connect_slots(self) -> None:
        """
        连接各种信号与槽 \n
        """

        self.center_widget.option_selected.connect(self.packaging_task.handle_option)
        self.packaging_task.option_set.connect(self.packager.set_pyinstaller_args)
        self.packaging_task.option_set.connect(self.center_widget.handle_option_set)
        self.packaging_task.option_error.connect(self.center_widget.handle_option_error)
        self.packaging_task.ready_to_pack.connect(
            self.center_widget.handle_ready_to_pack
        )

        self.packager.args_settled.connect(
            lambda val: self.center_widget.pyinstaller_args_browser.enrich_args_text(
                val
            )
        )

        def run_packaging():
            self.packager.run_packaging_process()
            self.subprocess_dlg.show()

        self.center_widget.run_packaging_btn.clicked.connect(run_packaging)

        def handle_multifunction():
            """处理子进程对话框多功能按钮点击信号的槽 \n"""
            btn_text = self.subprocess_dlg.multifunction_btn.text()
            if btn_text == "取消":
                self.packager.subprocess.abort_process()
                self.subprocess_dlg.close()
            elif btn_text == "打开输出位置":
                dist_path = self.packaging_task.script_path.parent / "dist"
                if sys.platform.startswith("win32"):
                    os.startfile(dist_path)
                elif sys.platform.startswith("linux"):
                    subprocess.call(["xdg-open", dist_path])
                elif sys.platform.startswith("darwin"):
                    subprocess.call(["open", dist_path])

        self.subprocess_dlg.multifunction_btn.clicked.connect(handle_multifunction)
        self.packager.subprocess.output.connect(self.subprocess_dlg.handle_output)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        重写关闭事件，进行收尾清理 \n
        :param event: 关闭事件
        """

        self.packager.subprocess.abort_process()
        super(MainApp, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
