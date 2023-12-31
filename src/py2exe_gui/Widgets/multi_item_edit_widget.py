# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块包含一组供用户编辑多个文本条目的控件，用于实现 PyInstaller 的 --hidden-import 等可以多次调用的选项

`MultiItemEditWindow` 是最主要的类，提供一个左侧有条目展示与编辑、右侧有删减条目按钮的窗口

`MultiPkgEditWindow` 继承自 `MultiItemEditWindow`，多了一个浏览当前 Python 环境中已安装 Python 包的功能
"""

__all__ = ["MultiItemEditWindow", "MultiPkgEditWindow"]

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
    """用于添加多个条目的窗口控件，实现如 --hidden-import、--collect-submodules 等功能"""

    items_selected = Signal(list)  # 用户在添加条目窗口完成所有编辑后，提交的信号.完整数据类型为 list[str]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        # 条目列表控件
        self.item_list_widget = QListWidget(self)

        # 可选中且可编辑
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

    def _setup_ui(self) -> None:
        """处理 UI"""

        self.setWindowIcon(QIcon(QPixmap(":/Icons/Py2exe-GUI_icon_72px")))

        self.new_btn.setText("新建(&N)")
        self.delete_btn.setText("删除(&D)")

        self.ok_btn.setText("确定")
        self.cancel_btn.setText("取消")

    # noinspection DuplicatedCode
    def _setup_layout(self) -> None:
        """构建与设置布局管理器"""

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
        """构建各槽函数、连接信号"""

        @Slot()
        def handle_new_btn() -> None:
            """新建按钮点击的槽函数"""

            new_item = QListWidgetItem("")
            new_item.setFlags(self._QListWidgetItem_flag)
            self.item_list_widget.addItem(new_item)
            self.item_list_widget.editItem(new_item)

        @Slot()
        def handle_delete_btn() -> None:
            """删除按钮点击的槽函数"""

            self.item_list_widget.takeItem(self.item_list_widget.currentRow())

        @Slot()
        def handle_ok_btn() -> None:
            """确定按钮点击的槽函数，将用户编辑好的条目列表以信号方式传出，并自身关闭窗口"""

            self.items_selected.emit(self._submit())
            self.close()

        self.new_btn.clicked.connect(handle_new_btn)
        self.delete_btn.clicked.connect(handle_delete_btn)

        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(handle_ok_btn)

    def _submit(self) -> list[str]:
        """将控件界面内容整理为字符串列表，准备提交

        会自动删去空白行

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
        """从给定的条目列表加载界面控件，用于打开先前已保存过的条目

        :param items: 条目列表
        """

        self.item_list_widget.clear()

        for item in items:
            list_widget_item = QListWidgetItem(item)
            list_widget_item.setFlags(self._QListWidgetItem_flag)
            self.item_list_widget.addItem(list_widget_item)


class MultiPkgEditWindow(MultiItemEditWindow):
    """用于添加多个Python模块条目的窗口控件，实现如 --hidden-import 等选项

    相比MultiItemEditWindow，主要是多了一个浏览当前 Python 环境中所有已安装第三方包
    并将包名作为条目添加的功能
    """

    def __init__(
        self, pkg_browser_dlg: PkgBrowserDlg, parent: Optional[QWidget] = None
    ) -> None:
        """
        :param pkg_browser_dlg: PkgBrowserDlg 实例，用于显示已安装包的列表
        :param parent: 父控件对象
        """

        # TODO 新增一种可以由用户选中的已安装包浏览器，并替代目前的 PkgBrowserDlg

        self.browse_pkg_button = QPushButton()
        self.pkg_browser_dlg = pkg_browser_dlg
        super().__init__(parent)

    def _setup_ui(self) -> None:
        """处理 UI"""

        super()._setup_ui()
        self.browse_pkg_button.setText("浏览包(&B)")

    def _setup_layout(self) -> None:
        """构建与设置布局管理器"""

        super()._setup_layout()
        self.btn_group_boxlayout.insertWidget(2, self.browse_pkg_button)

    def _connect_slots(self) -> None:
        """构建各槽函数、连接信号"""

        super()._connect_slots()
        self.browse_pkg_button.clicked.connect(self.pkg_browser_dlg.exec)
