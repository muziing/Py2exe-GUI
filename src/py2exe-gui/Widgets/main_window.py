import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QStatusBar

from .center_widget import CenterWidget
from .dialog_widgets import AboutMessage


class MainWindow(QMainWindow):
    """主界面主窗口"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.center_widget = CenterWidget(self)
        self.status_bar = QStatusBar(self)
        self.menu_bar = QMenuBar(self)

        self._setup()

    def _setup(self) -> None:
        """
        设置主窗口
        """

        self.setWindowTitle("Py2exe-GUI")
        # self.resize(800, 600)
        self.setWindowIcon(QIcon("../Resources/Icons/Python_128px.png"))  # GNOME下不生效

        self._setup_menu_bar()
        self._setup_status_bar()

        self.setCentralWidget(self.center_widget)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)

    def _setup_menu_bar(self) -> None:
        """
        配置主窗口菜单栏 \n
        :return: None
        """

        file_menu = self.menu_bar.addMenu("文件")
        file_menu.addAction("打开……")
        file_menu.addSeparator()
        file_menu.addAction("退出程序", self.close)  # 直接调用close可能整个程序并未完全退出

        about_menu = self.menu_bar.addMenu("关于")
        about_menu.addAction("关于本程序", AboutMessage(self).exec)
        about_menu.addAction("关于 &Qt", QApplication.aboutQt)

    def _setup_status_bar(self) -> None:
        """
        配置主窗口状态栏 \n
        :return: None
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
