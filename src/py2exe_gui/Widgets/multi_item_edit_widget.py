# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from typing import Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .dialog_widgets import PkgBrowserDlg


class MultiItemEditWindow(QWidget):
    """
    用于添加多个条目的窗口控件，实现如 --hidden-import、--collect-submodules 等功能 \n
    """

    items_selected = Signal(list)  # 用户在添加条目窗口完成所有编辑后，提交的信号.完整数据类型为 list[str]

    def __init__(self, parent: Optional[QWidget] = None):
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        # 条目列表控件
        self.item_list_widget = QListWidget(self)

        self._QListWidgetItem_flag = (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEditable
        )

        # 编辑功能按键
        self.new_btn = QPushButton(self)
        self.delete_btn = QPushButton(self)

        # 整个窗口的确认和取消键
        self.ok_btn = QPushButton(self)
        self.cancel_btn = QPushButton(self)

        self._setup_ui()
        self._setup_layout()
        self._connect_slots()

    def _setup_ui(self):
        """
        处理 UI \n
        """

        self.setWindowIcon(QIcon(QPixmap(":/Icons/Py2exe-GUI_icon_72px")))

        self.new_btn.setText("新建(&N)")
        self.delete_btn.setText("删除(&D)")

        self.ok_btn.setText("确定")
        self.cancel_btn.setText("取消")

    # noinspection DuplicatedCode
    def _setup_layout(self):
        """
        构建与设置布局管理器 \n
        """

        btn_group_boxlayout = QVBoxLayout()
        self.btn_group_boxlayout = btn_group_boxlayout
        btn_group_boxlayout.addWidget(self.new_btn)
        btn_group_boxlayout.addWidget(self.delete_btn)
        btn_group_boxlayout.addStretch(10)

        upper_box = QHBoxLayout()
        upper_box.addWidget(self.item_list_widget)
        upper_box.addLayout(btn_group_boxlayout)

        lower_box = QHBoxLayout()
        lower_box.addStretch(10)
        lower_box.addWidget(self.ok_btn)
        lower_box.addWidget(self.cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_box)
        main_layout.addLayout(lower_box)

        self.setLayout(main_layout)

    def _connect_slots(self) -> None:
        """
        构建各槽函数、连接信号 \n
        """

        @Slot()
        def handle_new_btn():
            new_item = QListWidgetItem("")
            new_item.setFlags(self._QListWidgetItem_flag)
            self.item_list_widget.addItem(new_item)
            self.item_list_widget.editItem(new_item)

        @Slot()
        def handle_delete_btn():
            self.item_list_widget.takeItem(self.item_list_widget.currentRow())

        @Slot()
        def handle_ok_btn():
            self.items_selected.emit(self._submit())
            self.close()

        self.new_btn.clicked.connect(handle_new_btn)
        self.delete_btn.clicked.connect(handle_delete_btn)

        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(handle_ok_btn)

    def _submit(self) -> list[str]:
        """
        将控件界面内容整理为字符串列表，准备提交 \n
        会自动删去空白行 \n
        :return: 条目列表
        """

        item_list = []

        for row in range(self.item_list_widget.count()):
            item_text = self.item_list_widget.item(row).text()
            if item_text == "":
                self.item_list_widget.takeItem(row)
            else:
                item_list.append(item_text)

        return item_list

    def load_items(self, items: list[str]) -> None:
        """
        从给定的条目列表加载界面控件，用于打开先前已保存过的条目
        :param items: 条目列表
        """

        self.item_list_widget.clear()

        for item in items:
            list_widget_item = QListWidgetItem(item)
            list_widget_item.setFlags(self._QListWidgetItem_flag)
            self.item_list_widget.addItem(list_widget_item)


class MultiPkgEditWindow(MultiItemEditWindow):
    """
    用于添加多个Python模块条目的窗口控件，实现如 --hidden-import 等选项 \n
    相比MultiItemEditWindow，主要是多了一个浏览当前 Python 环境中所有已安装第三方包
    并将包名作为条目添加的功能 \n
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        :param parent: 父控件对象
        """

        self.browse_pkg_button = QPushButton()
        self.pkg_browser_dlg = PkgBrowserDlg()
        super().__init__(parent)

    def _setup_ui(self):
        """
        处理 UI \n
        """

        super()._setup_ui()
        self.browse_pkg_button.setText("浏览包(&B)")

    def _setup_layout(self):
        super()._setup_layout()
        self.btn_group_boxlayout.insertWidget(2, self.browse_pkg_button)

    def _connect_slots(self) -> None:
        """
        构建各槽函数、连接信号 \n
        """

        super()._connect_slots()

        self.browse_pkg_button.clicked.connect(self.pkg_browser_dlg.exec)
