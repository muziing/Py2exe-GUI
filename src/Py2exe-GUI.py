import sys

from PySide6.QtWidgets import QApplication

from py2exe_gui.__main__ import MainApp

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
