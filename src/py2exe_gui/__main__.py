# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import sys

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication

from .Constants.platform_constants import get_platform
from .Core import Packaging, PackagingTask
from .Resources import compiled_resources  # type: ignore
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

        center_widget = self.center_widget
        packaging_task = self.packaging_task
        packager = self.packager

        center_widget.option_selected.connect(packaging_task.handle_option)
        packaging_task.option_set.connect(packager.set_pyinstaller_args)
        packaging_task.option_set.connect(center_widget.handle_option_set)
        packaging_task.option_error.connect(center_widget.handle_option_error)
        packaging_task.ready_to_pack.connect(center_widget.handle_ready_to_pack)
        packager.args_settled.connect(
            lambda val: center_widget.pyinstaller_args_browser.enrich_args_text(val)
        )
        packager.subprocess.output.connect(self.subprocess_dlg.handle_output)

    def closeEvent(self, event: QCloseEvent) -> None:
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
