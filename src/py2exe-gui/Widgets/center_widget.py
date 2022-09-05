import sys

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
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

from .dialog_widgets import IconFileDlg, ScriptFileDlg


class CenterWidget(QWidget):
    """主界面的中央控件"""

    # 自定义信号
    option_selected = QtCore.Signal(tuple)

    def __init__(self, parent: QMainWindow = None) -> None:
        super(CenterWidget, self).__init__(parent)

        self.script_path_label = QLabel(self)
        self.script_file_dlg = ScriptFileDlg(self)
        self.script_browse_btn = QPushButton(self)
        self.script_path_le = QLineEdit(self)

        self.fd_label = QLabel(self)
        self.one_dir_btn = QRadioButton(self)
        self.one_file_btn = QRadioButton(self)
        self.fd_group = QButtonGroup(self)

        self.icon_path_label = QLabel(self)
        self.icon_file_dlg = IconFileDlg(self)
        self.icon_browse_btn = QPushButton(self)
        self.icon_path_le = QLineEdit(self)

        # Windows/MacOS 独占，注意！！！
        self.console_checkbox = QCheckBox(self)

        self.run_packaging_btn = QPushButton(self)

        self.setup_ui()
        self.connect_slots()
        self._set_layout()

    def setup_ui(self) -> None:
        """
        设置各种控件的属性 \n
        :return: None
        """

        self.script_path_label.setText("脚本路径")
        self.script_path_le.setReadOnly(True)
        self.script_path_le.setPlaceholderText("Python入口文件路径")
        self.script_browse_btn.setText("浏览")

        self.fd_label.setText("单文件/单目录")
        self.one_dir_btn.setText("打包至单个目录")
        self.one_dir_btn.setChecked(True)
        self.one_file_btn.setText("打包至单个文件")
        self.fd_group.addButton(self.one_dir_btn, 0)
        self.fd_group.addButton(self.one_file_btn, 1)

        self.icon_path_label.setText("图标路径")
        self.icon_path_le.setReadOnly(True)
        self.icon_path_le.setPlaceholderText("图标文件路径")
        self.icon_browse_btn.setText("浏览")

        # Windows/MacOS 独占，注意！！！
        self.console_checkbox.setText("为标准I/O启用终端")
        self.console_checkbox.setChecked(True)

        self.run_packaging_btn.setText("运行打包！")
        self.run_packaging_btn.setEnabled(False)

    def connect_slots(self) -> None:
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
            # TODO 验证有效性
            self.script_path_le.setText(file_path)
            self.parent().statusBar().showMessage(f"打开脚本路径：{file_path}")
            self.option_selected.emit(("script_path", file_path))

        self.script_browse_btn.clicked.connect(self.script_file_dlg.open)  # type: ignore
        self.script_file_dlg.fileSelected.connect(script_file_selected)  # type: ignore

        @QtCore.Slot(int)
        def one_fd_selected(btn_id: int):
            if btn_id == 0:
                print("One Dir")
            elif btn_id == 1:
                print("One File")

        self.fd_group.idClicked.connect(one_fd_selected)  # type: ignore

        @QtCore.Slot(str)
        def icon_file_selected(file_path: str) -> None:
            """
            图标文件完成选择的槽函数
            :param file_path: 图标路径
            :return: None
            """
            # TODO 验证有效性
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
        main_layout.addLayout(fd_layout)
        main_layout.addWidget(self.console_checkbox)
        main_layout.addLayout(icon_layout)
        main_layout.addWidget(self.run_packaging_btn)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CenterWidget()
    window.show()
    sys.exit(app.exec())
