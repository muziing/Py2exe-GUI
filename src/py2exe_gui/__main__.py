import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from py2exe_gui.Core.packaging import Packaging
from py2exe_gui.Widgets.dialog_widgets import SubProcessDlg
from py2exe_gui.Widgets.main_window import MainWindow


class MainApp(MainWindow):
    """
    主程序
    """

    def __init__(self, *args, **kwargs) -> None:
        super(MainApp, self).__init__(*args, **kwargs)

        self.packager = Packaging(self)

        self.packager.args_settled.connect(
            lambda val: self.center_widget.pyinstaller_args_browser.enrich_args_text(
                val
            )
        )
        self.center_widget.option_selected.connect(self.packager.set_pyinstaller_args)

        self.subprocess_dlg = SubProcessDlg(self)

        def run_packaging():
            self.packager.run_packaging_process()
            self.subprocess_dlg.show()

        self.center_widget.run_packaging_btn.clicked.connect(run_packaging)
        self.packager.subprocess.output.connect(self.subprocess_dlg.handle_output)

        self.status_bar.showMessage("就绪")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        重写关闭事件，进行收尾清理 \n
        :param event: 关闭事件
        """

        self.packager.subprocess.abort_process()
        super(MainApp, self).closeEvent(event)


app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
