import sys

from Core import Packaging
from PySide6.QtWidgets import QApplication
from Widgets import MainWindow


class MainApp(MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.packager = Packaging()

        self.center_widget.option_selected.connect(self.packager.get_pyinstaller_args)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
