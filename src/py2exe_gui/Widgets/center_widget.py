# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块主要包含主界面中央控件类

CenterWidget 是主要类，定义了各种界面控件及其大部分信号与槽功能

WinMacCenterWidget 继承自 CenterWidget，额外添加了仅 Windows 和 macOS 平台才支持的
PyInstaller 功能所对应的控件及其槽函数
"""

__all__ = ["CenterWidget", "WinMacCenterWidget"]

from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..Constants import PyInstOpt
from ..Core import InterpreterValidator
from ..Utilities import PyEnv
from .add_data_widget import AddDataWindow
from .arguments_browser import ArgumentsBrowser
from .dialog_widgets import (
    IconFileDlg,
    InterpreterFileDlg,
    PkgBrowserDlg,
    ScriptFileDlg,
)
from .multi_item_edit_widget import MultiPkgEditWindow
from .pyenv_combobox import PyEnvComboBox
from .pyinstaller_option_widget import load_pyinst_options


class CenterWidget(QWidget):
    """主界面的中央控件

    此类为可以实例化的基类，适用于所有平台。
    有专有功能的平台应继承此类，并重写对应方法来添加相关控件与功能。
    """

    # 自定义信号
    option_selected = QtCore.Signal(tuple)  # 用户通过界面控件选择选项后发射此信号

    # option_selected 实际类型为 tuple[PyinstallerArgs, str]

    def __init__(self, parent: QMainWindow) -> None:
        """
        :param parent: 父控件对象，应为主程序主窗口
        """

        super().__init__(parent)

        self.parent_widget = parent

        # 读取PyInstaller选项详细描述，用于各控件ToolTip
        self.option_dict = load_pyinst_options()  # TODO 待优化：避免重复加载

        # 展示已安装的包
        self.pkg_browser_dlg = PkgBrowserDlg()

        # 待打包的入口脚本
        self.script_path_label = QLabel()
        self.script_file_dlg = ScriptFileDlg()
        self.script_browse_btn = QPushButton()
        self.script_path_le = QLineEdit()

        # Python 解释器选择
        self.pyenv_combobox = PyEnvComboBox()
        self.pyenv_browse_btn = QPushButton()
        self.itp_dlg = InterpreterFileDlg()

        # 打包后输出的项目名称
        self.project_name_label = QLabel()
        self.project_name_le = QLineEdit()

        # 输出至单目录/单文件
        self.fd_label = QLabel()
        self.one_dir_btn = QRadioButton()
        self.one_file_btn = QRadioButton()
        self.fd_group = QButtonGroup()

        # 添加数据与二进制文件
        self.add_data_btn = QPushButton()
        self.add_data_dlg = AddDataWindow()
        self.data_item_list: list[AddDataWindow.data_item] = []
        self.add_binary_btn = QPushButton()
        self.add_binary_dlg = AddDataWindow()
        self.binary_item_list: list[AddDataWindow.data_item] = []

        # 添加隐式导入
        self.hidden_import_btn = QPushButton()
        self.hidden_import_dlg = MultiPkgEditWindow(self.pkg_browser_dlg)
        self.hidden_import_list: list[str] = []

        # 清理缓存与临时文件
        self.clean_checkbox = QCheckBox()

        # 预览生成的PyInstaller打包指令
        self.pyinstaller_args_browser = ArgumentsBrowser()

        # 打包按钮
        self.run_packaging_btn = QPushButton()

        self._setup_ui()
        self._connect_slots()
        self._set_layout()

    def _setup_ui(self) -> None:
        """设置各种控件的属性"""

        self.script_path_label.setText("待打包脚本：")
        self.script_path_le.setReadOnly(True)
        self.script_path_le.setPlaceholderText("Python入口文件路径")
        self.script_browse_btn.setText("浏览")
        self.script_browse_btn.setFixedWidth(80)

        self.pyenv_browse_btn.setText("浏览")
        self.pyenv_browse_btn.setFixedWidth(80)

        self.project_name_label.setText("项目名称：")
        self.project_name_le.setPlaceholderText("打包的应用程序名称")

        self.fd_label.setText("单文件/单目录：")
        self.one_dir_btn.setText("打包至单个目录")
        self.one_dir_btn.setChecked(True)  # 默认值
        self.one_file_btn.setText("打包至单个文件")
        self.fd_group.addButton(self.one_dir_btn, 0)
        self.fd_group.addButton(self.one_file_btn, 1)

        self.add_data_btn.setText("添加数据文件")
        self.add_binary_btn.setText("添加二进制文件")
        self.add_data_dlg.setWindowTitle("添加数据文件")
        self.add_binary_dlg.setWindowTitle("添加二进制文件")

        self.hidden_import_btn.setText("隐式导入")
        self.hidden_import_dlg.setWindowTitle("Hidden import")

        self.clean_checkbox.setText("清理")
        self.clean_checkbox.setChecked(False)
        self.pyinstaller_args_browser.setMaximumHeight(80)

        self.run_packaging_btn.setText("打包！")
        self.run_packaging_btn.setEnabled(False)

        # 将 PyInstaller 选项详情设置成各控件的 ToolTip
        if self.option_dict:
            opt = self.option_dict
            # TODO: 解绑文本文档中的option字符和此处opt的键
            self.project_name_label.setToolTip(opt["-n NAME, --name NAME"])
            self.one_dir_btn.setToolTip(opt["-D, --onedir"])
            self.one_file_btn.setToolTip(opt["-F, --onefile"])
            self.add_data_btn.setToolTip(opt["--add-data SOURCE:DEST"])
            self.add_binary_btn.setToolTip(opt["--add-binary SOURCE:DEST"])
            self.hidden_import_btn.setToolTip(
                opt["--hidden-import MODULENAME, --hiddenimport MODULENAME"]
            )
            self.clean_checkbox.setToolTip(opt["--clean"])

    # noinspection DuplicatedCode
    def _connect_slots(self) -> None:
        """定义、连接信号与槽"""

        @QtCore.Slot(str)
        def handle_script_file_selected(file_path: str) -> None:
            """脚本文件完成选择的槽函数

            :param file_path: 脚本文件路径
            """

            self.option_selected.emit((PyInstOpt.script_path, file_path))

        @QtCore.Slot()
        def handle_project_name_selected() -> None:
            """输出程序名称完成输入的槽"""

            project_name: str = self.project_name_le.text()
            self.option_selected.emit((PyInstOpt.out_name, project_name))

        @QtCore.Slot(int)
        def handle_one_fd_selected(btn_id: int) -> None:
            """选择输出至单文件/单目录的槽

            :param btn_id: `fd_group` 按钮组中按钮的 id
            """

            if btn_id == 0:
                self.option_selected.emit((PyInstOpt.FD, "--onedir"))
                self.parent_widget.statusBar().showMessage("将打包至单个目录中")
            elif btn_id == 1:
                self.option_selected.emit((PyInstOpt.FD, "--onefile"))
                self.parent_widget.statusBar().showMessage("将打包至单个文件中")

        @QtCore.Slot()
        def handle_add_data_btn_clicked() -> None:
            """用户在界面点击添加数据按钮的槽函数"""

            self.add_data_dlg.load_data_item_list(self.data_item_list)
            self.add_data_dlg.show()

        @QtCore.Slot(list)
        def handle_add_data_selected(data_item_list: list) -> None:
            """用户完成了添加数据操作的槽函数"""

            self.data_item_list = data_item_list
            self.parent_widget.statusBar().showMessage("添加数据文件已更新")
            self.option_selected.emit((PyInstOpt.add_data, data_item_list))

        @QtCore.Slot()
        def handle_add_binary_btn_clicked() -> None:
            """用户在界面点击添加二进制文件按钮的槽函数"""

            self.add_binary_dlg.load_data_item_list(self.binary_item_list)
            self.add_binary_dlg.show()

        @QtCore.Slot(list)
        def handle_add_binary_selected(binary_item_list: list) -> None:
            """用户完成了添加二进制文件操作的槽函数"""

            self.binary_item_list = binary_item_list
            self.parent_widget.statusBar().showMessage("添加二进制文件已更新")
            self.option_selected.emit((PyInstOpt.add_binary, binary_item_list))

        @QtCore.Slot()
        def handle_hidden_import_btn_clicked() -> None:
            """点击隐式导入按钮的槽函数"""

            self.hidden_import_dlg.show()

        @QtCore.Slot(list)
        def handle_hidden_import_selected(hidden_import_list: list[str]) -> None:
            """用户完成了隐式导入编辑操作的槽函数

            :param hidden_import_list: 隐式导入项列表
            """

            self.hidden_import_list = hidden_import_list
            self.parent_widget.statusBar().showMessage("隐式导入已更新")
            self.option_selected.emit((PyInstOpt.hidden_import, hidden_import_list))

        @QtCore.Slot(bool)
        def handle_clean_selected(selected: bool) -> None:
            """选择了清理缓存复选框的槽

            :param selected: 是否勾选了 clean 复选框
            """

            if selected:
                self.option_selected.emit((PyInstOpt.clean, "--clean"))
                self.parent_widget.statusBar().showMessage("构建前将清理缓存与临时文件")
            else:
                self.option_selected.emit((PyInstOpt.clean, ""))
                self.parent_widget.statusBar().showMessage("不会删除缓存与临时文件")

        # 连接信号与槽
        # 入口脚本文件
        self.script_browse_btn.clicked.connect(self.script_file_dlg.open)
        self.script_file_dlg.fileSelected.connect(handle_script_file_selected)

        # 添加 Python 解释器
        self.pyenv_browse_btn.clicked.connect(self.itp_dlg.open)
        self.itp_dlg.fileSelected.connect(self._handle_itp_file_selected)

        # 项目名称
        self.project_name_le.editingFinished.connect(handle_project_name_selected)

        # 单目录/单文件模式
        self.fd_group.idClicked.connect(handle_one_fd_selected)

        # 添加数据文件与二进制文件
        self.add_data_btn.clicked.connect(handle_add_data_btn_clicked)
        self.add_data_dlg.data_selected.connect(handle_add_data_selected)
        self.add_binary_btn.clicked.connect(handle_add_binary_btn_clicked)
        self.add_binary_dlg.data_selected.connect(handle_add_binary_selected)

        # 隐式导入
        self.hidden_import_btn.clicked.connect(handle_hidden_import_btn_clicked)
        self.hidden_import_dlg.items_selected.connect(handle_hidden_import_selected)

        # 清理
        self.clean_checkbox.toggled.connect(handle_clean_selected)

    # noinspection DuplicatedCode
    def _set_layout(self) -> None:
        """设置布局管理器"""

        self.main_layout = QVBoxLayout()

        script_layout = QGridLayout()
        script_layout.addWidget(self.script_path_label, 0, 0, 1, 2)
        script_layout.addWidget(self.script_path_le, 1, 0)
        script_layout.addWidget(self.script_browse_btn, 1, 1)

        pyenv_layout = QHBoxLayout()
        pyenv_layout.addWidget(self.pyenv_combobox)
        pyenv_layout.addWidget(self.pyenv_browse_btn)

        name_layout = QVBoxLayout()
        name_layout.addWidget(self.project_name_label)
        name_layout.addWidget(self.project_name_le)

        fd_layout = QGridLayout()
        fd_layout.addWidget(self.fd_label, 0, 0, 1, 2)
        fd_layout.addWidget(self.one_dir_btn, 1, 0)
        fd_layout.addWidget(self.one_file_btn, 1, 1)

        add_btn_layout = QHBoxLayout()
        add_btn_layout.addWidget(self.add_data_btn)
        add_btn_layout.addWidget(self.add_binary_btn)

        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(script_layout)
        self.main_layout.addLayout(pyenv_layout)
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(name_layout)
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(fd_layout)
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(add_btn_layout)
        self.main_layout.addStretch(10)
        self.main_layout.addWidget(self.hidden_import_btn)
        self.main_layout.addStretch(10)
        self.main_layout.addWidget(self.clean_checkbox)
        self.main_layout.addStretch(10)
        self.main_layout.addWidget(self.pyinstaller_args_browser)
        self.main_layout.addWidget(self.run_packaging_btn)

        self.setLayout(self.main_layout)

    @QtCore.Slot(tuple)
    def handle_option_set(self, option: tuple[PyInstOpt, str]) -> None:
        """处理option_set信号的槽，根据已经成功设置的选项调整界面

        :param option: 选项键值对
        """

        option_key, option_value = option

        if option_key == PyInstOpt.script_path:
            script_path = Path(option_value)
            self.script_path_le.setText(script_path.name)
            self.parent_widget.statusBar().showMessage(
                f"打开脚本路径：{str(script_path.absolute())}"
            )
            self.add_data_dlg.set_work_dir(script_path.parent)
            self.add_binary_dlg.set_work_dir(script_path.parent)

        elif option_key == PyInstOpt.out_name:
            self.project_name_le.setText(option_value)
            self.parent_widget.statusBar().showMessage(f"已将项目名设置为：{option_value}")

    @QtCore.Slot(PyInstOpt)
    def handle_option_error(self, option: PyInstOpt) -> None:
        """处理option_error信号的槽，重置设置失败的选项对应的界面，并向用户发出警告

        :param option: 选项
        """

        # 清空重置该项的输入控件，并弹出警告窗口，等待用户重新输入
        if option == PyInstOpt.script_path:
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

    @QtCore.Slot(bool)
    def handle_ready_to_pack(self, ready: bool) -> None:
        """处理 ready_to_pack 信号的槽

        :param ready: 是否可以进行打包
        """

        self.run_packaging_btn.setEnabled(ready)

    @QtCore.Slot(str)
    def _handle_itp_file_selected(self, file_path: str) -> None:
        """Python解释器文件完成选择的槽函数

        首先对用户选择的文件进行有效性判断：
        若有效则以此创建新的 PyEnv 对象、设置到下拉框中并选中；
        若无效则弹出错误警告对话框，要求重新选择文件；

        :param file_path: 选择的解释器文件路径
        """

        itp_path = Path(file_path).absolute()

        # 首先判断用户选择的路径是否已在当前存储的列表中，如在则不添加直接返回
        for index in range(self.pyenv_combobox.count()):
            exist_env: PyEnv = self.pyenv_combobox.itemData(index)
            if str(itp_path) == exist_env.exe_path:
                return

        if InterpreterValidator.validate(itp_path):
            # 用户选择的解释器有效
            new_pyenv = PyEnv(itp_path, type_=None)

            # 但在该环境中没有安装 PyInstaller，询问用户是否继续操作
            if not new_pyenv.pkg_installed("pyinstaller"):
                result = QMessageBox.warning(
                    self.parent_widget,
                    "警告",
                    "在该 Python 环境中似乎没有安装 Pyinstaller，" "是否仍要继续？",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Cancel,
                )
                if result == QMessageBox.StandardButton.Cancel:
                    return

            self.pyenv_combobox.addItem(*self.pyenv_combobox.gen_item(new_pyenv))
            self.pyenv_combobox.setCurrentIndex(self.pyenv_combobox.count() - 1)

        else:
            # 用户选择的解释器无效
            self.itp_dlg.close()
            result = QMessageBox.critical(
                self.parent_widget,
                "错误",
                "选择的不是有效的Python解释器，请重新选择！",
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Ok,
            )
            if result == QMessageBox.StandardButton.Ok:
                self.itp_dlg.exec()


class WinMacCenterWidget(CenterWidget):
    """包含 Windows 与 MacOS 特有功能的主界面中央控件

    适用于所有平台功能的控件已由基类 `CenterWidget` 提供，此类仅实现平台特有功能对应的控件
    """

    def __init__(self, parent=QMainWindow):
        """
        :param parent: 父控件对象，应为主程序主窗口
        """

        # 应用图标
        self.icon_path_label = QLabel()
        self.icon_file_dlg = IconFileDlg()
        self.icon_browse_btn = QPushButton()
        self.icon_path_le = QLineEdit()

        # 是否为stdio启用终端
        self.console_checkbox = QCheckBox()

        super().__init__(parent)

    def _setup_ui(self) -> None:
        """设置各种控件的属性"""

        super()._setup_ui()

        self.icon_path_label.setText("应用图标：")
        self.icon_path_le.setReadOnly(True)
        self.icon_path_le.setPlaceholderText("图标文件路径")
        self.icon_browse_btn.setText("浏览")
        self.icon_browse_btn.setFixedWidth(80)

        self.console_checkbox.setText("为标准I/O启用终端")
        self.console_checkbox.setChecked(True)  # 默认值

        # 将 PyInstaller 选项详情设置成各控件的 ToolTip
        if self.option_dict:
            opt = self.option_dict
            self.icon_path_label.setToolTip(
                opt[
                    '-i <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">, '
                    "--icon <FILE.ico or FILE.exe,"
                    'ID or FILE.icns or Image or "NONE">'
                ]
            )
            self.console_checkbox.setToolTip(opt["-c, --console, --nowindowed"])

    def _connect_slots(self) -> None:
        """定义、连接信号与槽"""

        super()._connect_slots()

        @QtCore.Slot(str)
        def handle_icon_file_selected(file_path: str) -> None:
            """
            图标文件完成选择的槽函数 \n
            :param file_path: 图标路径
            """

            self.option_selected.emit((PyInstOpt.icon_path, file_path))

        @QtCore.Slot(bool)
        def handle_console_selected(console: bool) -> None:
            """选择打包的程序是否为stdio启用终端的槽

            :param console: 是否启用终端
            """

            if console:
                self.option_selected.emit((PyInstOpt.console, "--console"))
                self.parent_widget.statusBar().showMessage("将为打包程序的 stdio 启用终端")
            else:
                self.option_selected.emit((PyInstOpt.console, "--windowed"))
                self.parent_widget.statusBar().showMessage("不会为打包程序的 stdio 启用终端")

        # 图标文件
        self.icon_browse_btn.clicked.connect(self.icon_file_dlg.open)
        self.icon_file_dlg.fileSelected.connect(handle_icon_file_selected)

        # 是否启用 stdio 终端
        self.console_checkbox.toggled.connect(handle_console_selected)

    # noinspection DuplicatedCode
    def _set_layout(self) -> None:
        """设置布局管理器"""

        super()._set_layout()

        icon_layout = QGridLayout()
        icon_layout.addWidget(self.icon_path_label, 0, 0, 1, 2)
        icon_layout.addWidget(self.icon_path_le, 1, 0)
        icon_layout.addWidget(self.icon_browse_btn, 1, 1)

        self.main_layout.insertWidget(7, self.console_checkbox)
        self.main_layout.addStretch(10)
        self.main_layout.insertLayout(8, icon_layout)

    @QtCore.Slot(tuple)
    def handle_option_set(self, option: tuple[PyInstOpt, str]) -> None:
        """处理option_set信号的槽，根据已经成功设置的选项调整界面

        :param option: 选项键值对
        """

        super().handle_option_set(option)

        option_key, option_value = option

        if option_key == PyInstOpt.script_path:
            # 根据入口脚本路径，重新设置图标文件对话框的初始路径
            script_path = Path(option_value)
            self.icon_file_dlg.setDirectory(str(script_path.parent.absolute()))

        elif option_key == PyInstOpt.icon_path:
            icon_path = Path(option_value)
            self.icon_path_le.setText(icon_path.name)
            self.parent_widget.statusBar().showMessage(
                f"打开图标路径：{str(icon_path.absolute())}"
            )

    @QtCore.Slot(PyInstOpt)
    def handle_option_error(self, option: PyInstOpt) -> None:
        """处理option_error信号的槽，重置设置失败的选项对应的界面，并向用户发出警告

        :param option: 选项
        """

        super().handle_option_error(option)

        if option == PyInstOpt.icon_path:
            self.icon_file_dlg.close()
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
