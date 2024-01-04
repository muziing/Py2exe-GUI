# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块主要包含 `MainWindow` 主窗口控件，定义并配置了一个有工具栏、中央控件、状态栏的主窗口

仅包含控件（前端界面）部分，不包含打包任务等（后端）功能
"""

__all__ = ["open_url", "MainWindow"]

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QStatusBar

from ..Constants import RUNTIME_INFO, APP_URLs, AppConstant, Platform
from ..Utilities.qobject_tr import QObjTr
from .center_widget import CenterWidget, WinMacCenterWidget
from .dialog_widgets import AboutDlg


def open_url(url: str) -> None:
    """辅助函数，在系统默认浏览器中打开 `url`

    :param url: 待打开的URL
    """

    QDesktopServices.openUrl(QUrl(url))


class MainWindow(QObjTr, QMainWindow):
    """
    主界面主窗口
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.center_widget: CenterWidget
        if RUNTIME_INFO.platform in (Platform.windows, Platform.macos):
            self.center_widget = WinMacCenterWidget(self)
        else:
            self.center_widget = CenterWidget(self)

        self.menu_bar = QMenuBar(self)
        self.status_bar = QStatusBar(self)

        self.setCentralWidget(self.center_widget)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)

        self._setup()

    def _setup(self) -> None:
        """设置主窗口"""

        self.setWindowTitle("Py2exe-GUI")
        self.setMinimumSize(350, 430)
        # self.resize(800, 600)
        self.setWindowIcon(QIcon(QPixmap(":/Icons/Py2exe-GUI_icon_72px")))

        self._setup_menu_bar()
        self._setup_status_bar()

    def _setup_menu_bar(self) -> None:
        """配置主窗口菜单栏"""

        file_menu = self.menu_bar.addMenu(MainWindow.tr("&File"))
        file_menu.addAction(MainWindow.tr("Import Config From JSON File"))  # 暂时只为占位
        file_menu.addAction(MainWindow.tr("Export Config To JSON File"))  # 暂时只为占位
        file_menu.addSeparator()
        file_menu.addAction(MainWindow.tr("&Settings"))  # 暂时只为占位
        file_menu.addSeparator()
        file_menu.addAction(MainWindow.tr("&Exit"), self.close)

        help_menu = self.menu_bar.addMenu(MainWindow.tr("&Help"))

        help_menu.addAction(
            MainWindow.tr("PyInstaller Documentation"),
            lambda: open_url(APP_URLs["Pyinstaller_doc"]),
        )
        help_menu.addAction(
            MainWindow.tr("PyInstaller Options Details"),
            self.center_widget.pyinstaller_option_table.show,
        )
        help_menu.addSeparator()
        help_menu.addAction(
            MainWindow.tr("Report Bugs"), lambda: open_url(APP_URLs["BugTracker"])
        )

        about_menu = self.menu_bar.addMenu(MainWindow.tr("&About"))
        about_menu.addAction(MainWindow.tr("About This Program"), AboutDlg(self).exec)
        about_menu.addAction(MainWindow.tr("About &Qt"), QApplication.aboutQt)

    def _setup_status_bar(self) -> None:
        """配置主窗口状态栏"""

        # 在最右侧固定显示版本信息
        version_label = QLabel("V" + AppConstant.VERSION, self.status_bar)
        self.status_bar.insertPermanentWidget(0, version_label)
