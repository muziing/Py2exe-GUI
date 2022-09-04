import sys

from Core import run_packaging_process
from PySide6.QtWidgets import QApplication
from Widgets import MainWindow


class MainApp(MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)

        def test_slot(file: str):
            print(file)
            print(run_packaging_process(["-v"]))

        self.center_widget.script_file_dlg.fileSelected.connect(test_slot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
