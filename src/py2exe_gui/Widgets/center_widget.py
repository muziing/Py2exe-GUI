# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..Constants.packaging_constants import PyinstallerArgs
from ..Constants.platform_constants import PLATFORM
from .arguments_browser import ArgumentsBrowser
from .dialog_widgets import IconFileDlg, ScriptFileDlg


class CenterWidget(QWidget):
    """
    主界面的中央控件
    """

    # 自定义信号
    option_selected = QtCore.Signal(tuple)  # 用户通过界面控件选择选项后发射此信号

    def __init__(self, parent: QMainWindow) -> None:
        """
        :param parent: 父控件对象，应为主程序
        """

        super(CenterWidget, self).__init__(parent)

        self.parent_widget = parent

        # 根据运行平台不同，提供的控件也有所区别
        self.running_platform: PLATFORM = parent.running_platform  # type: ignore

        # 待打包的入口脚本
        self.script_path_label = QLabel()
        self.script_file_dlg = ScriptFileDlg()
        self.script_browse_btn = QPushButton()
        self.script_path_le = QLineEdit()

        # 打包后输出的项目名称
        self.project_name_label = QLabel()
        self.project_name_le = QLineEdit()

        # 输出至单目录/单文件
        self.fd_label = QLabel()
        self.one_dir_btn = QRadioButton()
        self.one_file_btn = QRadioButton()
        self.fd_group = QButtonGroup()

        # 应用图标（仅 Windows 与 macOS）
        if self.running_platform in (PLATFORM.windows, PLATFORM.macos):
            self.icon_path_label = QLabel()
            self.icon_file_dlg = IconFileDlg()
            self.icon_browse_btn = QPushButton()
            self.icon_path_le = QLineEdit()

        # 是否为stdio启用终端（仅 Windows 与 macOS）
        if self.running_platform in (PLATFORM.windows, PLATFORM.macos):
            self.console_checkbox = QCheckBox()

        # 预览生成的PyInstaller打包指令
        self.pyinstaller_args_browser = ArgumentsBrowser()

        # 打包按钮
        self.run_packaging_btn = QPushButton()

        self.setup_ui()
        self._connect_slots()
        self._set_layout()

    def setup_ui(self) -> None:
        """
        设置各种控件的属性 \n
        """

        self.script_path_label.setText("待打包脚本：")
        self.script_path_le.setReadOnly(True)
        self.script_path_le.setPlaceholderText("Python入口文件路径")
        self.script_browse_btn.setText("浏览")

        self.project_name_label.setText("项目名称：")
        self.project_name_le.setPlaceholderText("打包的应用程序名称")

        self.fd_label.setText("单文件/单目录：")
        self.one_dir_btn.setText("打包至单个目录")
        self.one_dir_btn.setChecked(True)  # 默认值
        self.one_file_btn.setText("打包至单个文件")
        self.fd_group.addButton(self.one_dir_btn, 0)
        self.fd_group.addButton(self.one_file_btn, 1)

        if self.running_platform in (PLATFORM.windows, PLATFORM.macos):
            self.icon_path_label.setText("应用图标：")
            self.icon_path_le.setReadOnly(True)
            self.icon_path_le.setPlaceholderText("图标文件路径")
            self.icon_browse_btn.setText("浏览")

            self.console_checkbox.setText("为标准I/O启用终端")
            self.console_checkbox.setChecked(True)  # 默认值

        self.pyinstaller_args_browser.setMaximumHeight(80)

        self.run_packaging_btn.setText("打包！")
        self.run_packaging_btn.setEnabled(False)

    def _connect_slots(self) -> None:
        """
        定义、连接信号与槽 \n
        """

        @QtCore.Slot(str)
        def script_file_selected(file_path: str) -> None:
            """
            脚本文件完成选择的槽函数 \n
            :param file_path: 脚本文件路径
            """

            self.option_selected.emit((PyinstallerArgs.script_path, file_path))

        @QtCore.Slot()
        def project_name_selected() -> None:
            """
            输出程序名称完成输入的槽 \n
            """

            project_name: str = self.project_name_le.text()
            self.option_selected.emit((PyinstallerArgs.out_name, project_name))

        @QtCore.Slot(int)
        def one_fd_selected(btn_id: int) -> None:
            """
            选择输出至单文件/单目录的槽 \n
            :param btn_id: fd_group按钮组中按钮的id
            """

            if btn_id == 0:
                self.option_selected.emit((PyinstallerArgs.FD, "--onedir"))
                self.parent_widget.statusBar().showMessage("将打包至单个目录中")
            elif btn_id == 1:
                self.option_selected.emit((PyinstallerArgs.FD, "--onefile"))
                self.parent_widget.statusBar().showMessage("将打包至单个文件中")

        @QtCore.Slot(bool)
        def console_selected(console: bool) -> None:
            """
            选择打包的程序是否为stdio启用终端的槽 \n
            :param console: 是否启用终端
            """

            if console:
                self.option_selected.emit((PyinstallerArgs.console, "--console"))
                self.parent_widget.statusBar().showMessage("将为打包程序的 stdio 启用终端")
            else:
                self.option_selected.emit((PyinstallerArgs.console, "--windowed"))
                self.parent_widget.statusBar().showMessage("不会为打包程序的 stdio 启用终端")

        @QtCore.Slot(str)
        def icon_file_selected(file_path: str) -> None:
            """
            图标文件完成选择的槽函数 \n
            :param file_path: 图标路径
            """

            self.option_selected.emit((PyinstallerArgs.icon_path, file_path))

        @QtCore.Slot()
        def run_packaging() -> None:
            """
            “运行打包”按钮的槽函数 \n
            """

            self.parent().packager.run_packaging_process()
            self.parent().subprocess_dlg.show()

        # 连接信号与槽
        self.script_browse_btn.clicked.connect(self.script_file_dlg.open)  # type: ignore
        self.script_file_dlg.fileSelected.connect(script_file_selected)  # type: ignore
        self.project_name_le.editingFinished.connect(project_name_selected)  # type: ignore
        self.fd_group.idClicked.connect(one_fd_selected)  # type: ignore
        self.run_packaging_btn.clicked.connect(run_packaging)  # type: ignore

        if self.running_platform in (PLATFORM.windows, PLATFORM.macos):
            self.icon_browse_btn.clicked.connect(self.icon_file_dlg.open)  # type: ignore
            self.icon_file_dlg.fileSelected.connect(icon_file_selected)  # type: ignore
            self.console_checkbox.toggled.connect(console_selected)  # type: ignore

    @QtCore.Slot(tuple)
    def handle_option_set(self, option: tuple[str, str]) -> None:
        """
        处理option_set信号的槽，根据已经成功设置的选项调整界面 \n
        :param option: 选项键值对
        """

        option_key, option_value = option

        if option_key == PyinstallerArgs.script_path:
            script_path = Path(option_value)
            self.script_path_le.setText(script_path.name)
            self.parent_widget.statusBar().showMessage(
                f"打开脚本路径：{str(script_path.resolve())}"
            )

        elif option_key == PyinstallerArgs.icon_path:
            icon_path = Path(option_value)
            self.icon_path_le.setText(icon_path.name)
            self.parent_widget.statusBar().showMessage(
                f"打开图标路径：{str(icon_path.resolve())}"
            )

        elif option_key == PyinstallerArgs.out_name:
            self.project_name_le.setText(option_value)
            self.parent_widget.statusBar().showMessage(f"已将项目名设置为：{option_value}")

    @QtCore.Slot(PyinstallerArgs)
    def handle_option_error(self, option: PyinstallerArgs) -> None:
        """
        处理option_error信号的槽，重置设置失败的选项对应的界面，并向用户发出警告 \n
        :param option: 选项
        """

        # 清空重置该项的输入控件，并弹出警告窗口，等待用户重新输入
        if option == PyinstallerArgs.script_path:
            self.script_file_dlg.close()

            # 警告对话框
            result = QMessageBox.critical(
                self.parent_widget,
                "错误",
                "选择的不是有效的Python脚本文件，请重新选择！",
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Ok,
            )
            if result == QMessageBox.StandardButton.Cancel:
                self.script_path_le.clear()
                self.project_name_le.clear()
            elif result == QMessageBox.StandardButton.Ok:
                self.script_file_dlg.exec()

        elif option == PyinstallerArgs.icon_path:
            self.icon_file_dlg.close()

            # 警告对话框
            result = QMessageBox.critical(
                self.parent_widget,
                "错误",
                "选择的不是有效的图标文件，请重新选择！",
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Ok,
            )
            if result == QMessageBox.StandardButton.Cancel:
                self.icon_path_le.clear()
            elif result == QMessageBox.StandardButton.Ok:
                self.icon_file_dlg.exec()

    @QtCore.Slot(bool)
    def handle_ready_to_pack(self, ready: bool) -> None:
        """
        处理ready_to_pack信号的槽 \n
        :param ready: 是否可以进行打包
        """

        self.run_packaging_btn.setEnabled(ready)

    def _set_layout(self) -> None:
        """
        设置布局管理器 \n
        """

        script_layout = QGridLayout()
        script_layout.addWidget(self.script_path_label, 0, 0, 1, 2)
        script_layout.addWidget(self.script_path_le, 1, 0)
        script_layout.addWidget(self.script_browse_btn, 1, 1)

        name_layout = QVBoxLayout()
        name_layout.addWidget(self.project_name_label)
        name_layout.addWidget(self.project_name_le)

        fd_layout = QGridLayout()
        fd_layout.addWidget(self.fd_label, 0, 0, 1, 2)
        fd_layout.addWidget(self.one_dir_btn, 1, 0)
        fd_layout.addWidget(self.one_file_btn, 1, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(script_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(name_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(fd_layout)
        main_layout.addSpacing(10)

        if self.running_platform in (PLATFORM.windows, PLATFORM.macos):
            main_layout.addWidget(self.console_checkbox)
            main_layout.addSpacing(10)

            icon_layout = QGridLayout()
            icon_layout.addWidget(self.icon_path_label, 0, 0, 1, 2)
            icon_layout.addWidget(self.icon_path_le, 1, 0)
            icon_layout.addWidget(self.icon_browse_btn, 1, 1)
            main_layout.addLayout(icon_layout)

        main_layout.addSpacing(10)
        main_layout.addWidget(self.pyinstaller_args_browser)
        main_layout.addWidget(self.run_packaging_btn)
        self.setLayout(main_layout)
