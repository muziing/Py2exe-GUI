import sys

from Core import Packaging
from PySide6.QtWidgets import QApplication
from Widgets import MainWindow


class MainApp(MainWindow):
    """主程序"""

    def __init__(self, *args, **kwargs) -> None:
        super(MainApp, self).__init__(*args, **kwargs)

        self.packager = Packaging()

        self.center_widget.option_selected.connect(self.packager.get_pyinstaller_args)
        self.center_widget.run_packaging_btn.clicked.connect(
            self.packager.run_packaging_process
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
