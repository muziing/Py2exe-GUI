import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from .Constants.platform_constants import get_platform
from .Core import Packaging, PackagingTask
from .Resources.compiled_resources import *
from .Widgets import MainWindow, SubProcessDlg


class MainApp(MainWindow):
    """
    应用主程序 \n
    """

    def __init__(self, *args, **kwargs) -> None:
        self.running_platform = get_platform()  # 获取当前运行的平台信息
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
