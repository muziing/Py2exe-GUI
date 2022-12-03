# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import sys

from PySide6.QtWidgets import QApplication

from py2exe_gui.__main__ import MainApp

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
