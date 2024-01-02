# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""程序入口脚本
由于整个程序作为单一 Python 包发布，直接运行 py2exe_gui.__main__.py 会导致相对导入错误
需要在包外留有这个显式的入口模块来提供“通过运行某个 .py 文件启动程序”功能和 PyInstaller 打包入口脚本

Py2exe-GUI 启动方式：
    python Py2exe-GUI.py
或
    python -m py2exe_gui
"""

import sys

from PySide6.QtWidgets import QApplication

from py2exe_gui.__main__ import MainApp

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
