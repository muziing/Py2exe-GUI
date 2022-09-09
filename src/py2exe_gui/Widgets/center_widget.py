from PySide6 import QtCore
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from .arguments_browser import ArgumentsBrowser
from .dialog_widgets import IconFileDlg, ScriptFileDlg


class CenterWidget(QWidget):
    """主界面的中央控件"""

    # 自定义信号
    option_selected = QtCore.Signal(tuple)

    def __init__(self, parent: QMainWindow = None) -> None:
        super(CenterWidget, self).__init__(parent)

        # 待打包的入口脚本
        self.script_path_label = QLabel()
        self.script_file_dlg = ScriptFileDlg()
        self.script_browse_btn = QPushButton()
        self.script_path_le = QLineEdit()

        # 打包后输出的项目名称
        self.name_label = QLabel()
        self.name_le = QLineEdit()

        # 输出至单目录/单文件
        self.fd_label = QLabel()
        self.one_dir_btn = QRadioButton()
        self.one_file_btn = QRadioButton()
        self.fd_group = QButtonGroup()

        # 应用图标
        self.icon_path_label = QLabel()
        self.icon_file_dlg = IconFileDlg()
        self.icon_browse_btn = QPushButton()
        self.icon_path_le = QLineEdit()

        # Windows/MacOS 独占，注意后期处理成在Linux下不显示
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
        :return: None
        """

        self.script_path_label.setText("脚本路径：")
        self.script_path_le.setReadOnly(True)
        self.script_path_le.setPlaceholderText("Python入口文件路径")
        self.script_browse_btn.setText("浏览")

        self.name_label.setText("输出名称：")
        self.name_le.setPlaceholderText("打包的应用程序名称")

        self.fd_label.setText("单文件/单目录：")
        self.one_dir_btn.setText("打包至单个目录")
        self.one_dir_btn.setChecked(True)  # 默认值
        self.one_file_btn.setText("打包至单个文件")
        self.fd_group.addButton(self.one_dir_btn, 0)
        self.fd_group.addButton(self.one_file_btn, 1)

        self.icon_path_label.setText("图标路径：")
        self.icon_path_le.setReadOnly(True)
        self.icon_path_le.setPlaceholderText("图标文件路径")
        self.icon_browse_btn.setText("浏览")

        # Windows/MacOS 独占，注意！！！
        self.console_checkbox.setText("为标准I/O启用终端")
        self.console_checkbox.setChecked(True)  # 默认值

        self.pyinstaller_args_browser.setMaximumHeight(80)

        self.run_packaging_btn.setText("打包！")
        # TODO 完成输入检查前、子进程运行时打包按钮设置为不可用
        # self.run_packaging_btn.setEnabled(False)

    def _connect_slots(self) -> None:
        """
        定义、连接信号与槽 \n
        :return: None
        """

        @QtCore.Slot(str)
        def script_file_selected(file_path: str) -> None:
            """
            脚本文件完成选择的槽函数 \n
            :param file_path: 脚本文件路径
            :return: None
            """
            # TODO 验证有效性、将脚本名作为默认app名
            # 将字符串类型的文件路径转成pathlib型的？
            self.script_path_le.setText(file_path)
            self.parent().statusBar().showMessage(f"打开脚本路径：{file_path}")
            self.option_selected.emit(("script_path", file_path))

        self.script_browse_btn.clicked.connect(self.script_file_dlg.open)  # type: ignore
        self.script_file_dlg.fileSelected.connect(script_file_selected)  # type: ignore

        # FIXME 默认输出程序名称与入口脚本名称相同
        @QtCore.Slot(str)
        def project_name_selected() -> None:
            """
            输出程序名称完成输入的槽 \n
            :return: None
            """
            pro_name: str = self.name_le.text()
            self.option_selected.emit(("out_name", pro_name))

        self.name_le.editingFinished.connect(project_name_selected)  # type: ignore

        @QtCore.Slot(int)
        def one_fd_selected(btn_id: int) -> None:
            """
            选择输出至单文件/单目录的槽 \n
            :param btn_id: fd_group按钮组中按钮的id
            :return: None
            """
            if btn_id == 0:
                self.option_selected.emit(("FD", "One Dir"))
            elif btn_id == 1:
                self.option_selected.emit(("FD", "One File"))

        self.fd_group.idClicked.connect(one_fd_selected)  # type: ignore

        @QtCore.Slot(bool)
        def console_selected(console: bool) -> None:
            """
            选择打包的程序是否为stdio启用终端的槽 \n
            :param console: 是否启用终端
            :return: None
            """
            if console:
                self.option_selected.emit(("console", "console"))
            else:
                self.option_selected.emit(("console", "windowed"))

        self.console_checkbox.toggled.connect(console_selected)  # type: ignore

        @QtCore.Slot(str)
        def icon_file_selected(file_path: str) -> None:
            """
            图标文件完成选择的槽函数
            :param file_path: 图标路径
            :return: None
            """
            self.icon_path_le.setText(file_path)
            self.parent().statusBar().showMessage(f"打开图标路径：{file_path}")
            self.option_selected.emit(("icon_path", file_path))

        self.icon_browse_btn.clicked.connect(self.icon_file_dlg.open)  # type: ignore
        self.icon_file_dlg.fileSelected.connect(icon_file_selected)  # type: ignore

    def _set_layout(self) -> None:
        """
        设置布局管理器 \n
        :return: None
        """

        script_layout = QGridLayout()
        script_layout.addWidget(self.script_path_label, 0, 0, 1, 2)
        script_layout.addWidget(self.script_path_le, 1, 0)
        script_layout.addWidget(self.script_browse_btn, 1, 1)

        name_layout = QVBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_le)

        fd_layout = QGridLayout()
        fd_layout.addWidget(self.fd_label, 0, 0, 1, 2)
        fd_layout.addWidget(self.one_dir_btn, 1, 0)
        fd_layout.addWidget(self.one_file_btn, 1, 1)

        icon_layout = QGridLayout()
        icon_layout.addWidget(self.icon_path_label, 0, 0, 1, 2)
        icon_layout.addWidget(self.icon_path_le, 1, 0)
        icon_layout.addWidget(self.icon_browse_btn, 1, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(script_layout)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(fd_layout)
        main_layout.addWidget(self.console_checkbox)
        main_layout.addLayout(icon_layout)
        main_layout.addWidget(self.pyinstaller_args_browser)
        main_layout.addWidget(self.run_packaging_btn)
        self.setLayout(main_layout)
