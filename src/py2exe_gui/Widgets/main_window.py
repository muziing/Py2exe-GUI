from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QIcon
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
        self.setMinimumSize(320, 350)
        # self.resize(800, 600)
        self.setWindowIcon(QIcon("../Resources/Icons/Python_128px.png"))

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

        file_menu = self.menu_bar.addMenu("文件(&F)")
        file_menu.addAction("打开……")  # 暂时只为占位
        file_menu.addSeparator()
        file_menu.addAction("退出程序(&E)", self.close)  # 直接调用close可能整个程序并未完全退出？

        help_menu = self.menu_bar.addMenu("帮助(&H)")

        def open_url(url: str):
            """辅助函数，在系统默认浏览器中打开URL"""
            QDesktopServices.openUrl(QUrl(url))

        help_menu.addAction(
            "PyInstaller官方文档",
            lambda: open_url("https://pyinstaller.org/en/stable/usage.html"),
        )
        help_menu.addSeparator()
        help_menu.addAction(
            "报告Bug", lambda: open_url("https://github.com/muziing/Py2exe-GUI/issues")
        )

        about_menu = self.menu_bar.addMenu("关于(&A)")
        about_menu.addAction("关于本程序", AboutMessage(self).exec)
        about_menu.addAction("关于 &Qt", QApplication.aboutQt)

    def _setup_status_bar(self) -> None:
        """
        配置主窗口状态栏 \n
        :return: None
        """
        pass
