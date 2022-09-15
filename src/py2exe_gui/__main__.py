import sys

from PySide6.QtWidgets import QApplication

from .Core.packaging import Packaging
from .Widgets.main_window import MainWindow


class MainApp(MainWindow):
    """主程序"""

    def __init__(self, *args, **kwargs) -> None:
        super(MainApp, self).__init__(*args, **kwargs)

        self.packager = Packaging()

        self.packager.args_settled.connect(
            lambda val: self.center_widget.pyinstaller_args_browser.enrich_args_text(
                val
            )
        )

        self.center_widget.option_selected.connect(self.packager.get_pyinstaller_args)
        self.center_widget.run_packaging_btn.clicked.connect(
            self.packager.run_packaging_process
        )

        self.status_bar.showMessage("就绪")


app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
