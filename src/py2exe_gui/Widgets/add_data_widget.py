# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QItemSelectionModel, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class AddDataWindow(QWidget):
    """
    用于提供 PyInstaller --add-data 和 --add-binary 功能的窗口
    """

    # 类型别名
    data_item = tuple[Path, str]  # 数据条目，第一项为在文件系统中的路径，第二项为捆绑后环境中的路径

    # 自定义信号
    data_selected = Signal(list)  # 用户在添加数据窗口完成所有编辑后，提交的信号

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # 工作目录，应由主界面提供，默认为入口脚本所在目录；各种文件处理将以此作为相对路径起点
        self._work_dir: Path = Path(".").resolve()

        # 浏览系统文件/目录的文件对话框
        self.data_browse_dlg = QFileDialog(self)
        self.data_dir_browse_dlg = QFileDialog(self)

        # 条目表格，双列，每行为一条添加的数据
        self.item_table = QTableWidget(self)

        # 各种编辑功能按键
        self.new_btn = QPushButton(self)
        self.browse_btn = QPushButton(self)
        self.browse_dir_btn = QPushButton(self)
        self.delete_btn = QPushButton(self)

        # 整个窗口的确认和取消键
        self.ok_btn = QPushButton(self)
        self.cancel_btn = QPushButton(self)

        self._setup_ui()
        self._setup_layout()

        self.connect_slots()

    def _setup_ui(self):
        """
        处理 UI 内容 \n
        """

        self.setWindowTitle("添加文件")
        self.setMinimumWidth(550)

        self.data_browse_dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.data_dir_browse_dlg.setFileMode(QFileDialog.FileMode.Directory)

        self.item_table.setColumnCount(2)
        self.item_table.setRowCount(0)
        self.item_table.setHorizontalHeaderLabels(["SOURCE", "DEST"])
        self.item_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.item_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )

        self.new_btn.setText("新建(&N)")
        self.browse_btn.setText("浏览文件(&B)")
        self.browse_dir_btn.setText("浏览目录(&F)")
        self.delete_btn.setText("删除(&D)")

        self.ok_btn.setText("确定")
        self.cancel_btn.setText("取消")

    def _setup_layout(self):
        """
        构建与设置布局管理器 \n
        """

        btn_group_box = QVBoxLayout()
        btn_group_box.addWidget(self.new_btn)
        btn_group_box.addWidget(self.browse_btn)
        btn_group_box.addWidget(self.browse_dir_btn)
        btn_group_box.addWidget(self.delete_btn)
        btn_group_box.addStretch(10)

        upper_box = QHBoxLayout()
        upper_box.addWidget(self.item_table)
        upper_box.addLayout(btn_group_box)

        lower_box = QHBoxLayout()
        lower_box.addStretch(10)
        lower_box.addWidget(self.ok_btn)
        lower_box.addWidget(self.cancel_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_box)
        main_layout.addLayout(lower_box)

        self.setLayout(main_layout)

    def set_work_dir(self, work_dir_path: Path) -> None:
        self._work_dir = work_dir_path
        self.data_browse_dlg.setDirectory(str(work_dir_path))
        self.data_dir_browse_dlg.setDirectory(str(work_dir_path))

    def _submit(self) -> list[data_item]:
        """
        将当前界面上的所有配置项转换为 data_item 列表，准备提交给主界面和打包流使用 \n
        """

        all_data_item_list = []
        for row in range(self.item_table.rowCount()):
            path = Path(self.item_table.item(row, 0).text())
            dest = self.item_table.item(row, 1).text()
            all_data_item_list.append((path, dest))

        # print(all_data_item_list)  # 调试用
        return all_data_item_list

    def load_data_item_list(self, all_data_item_list: list[data_item]):
        """
        从 data_item 列表加载待添加的数据文件至界面控件
        """

        self.item_table.clear()
        self.item_table.setRowCount(len(all_data_item_list))
        for row, data_item in enumerate(all_data_item_list):
            source_item = QTableWidgetItem(str(data_item[0].resolve()))
            source_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
            )
            self.item_table.setItem(row, 0, source_item)
            self.item_table.setItem(row, 1, QTableWidgetItem(data_item[1]))

    def connect_slots(self):
        """
        构建各槽函数、连接信号 \n
        """

        @Slot()
        def new_btn_handle():
            # “新建”按钮槽函数
            row_count = self.item_table.rowCount()
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.item_table.setRowCount(row_count + 1)
            self.item_table.setItem(row_count, 0, item)
            self.item_table.setItem(row_count, 1, QTableWidgetItem("."))
            self.item_table.setCurrentCell(
                row_count, 0, QItemSelectionModel.SelectionFlag.Select
            )  # 自动选中新建行的第一列

        @Slot()
        def delete_btn_handle():
            # “删除”按钮槽函数
            self.item_table.removeRow(self.item_table.currentRow())

        @Slot()
        def browse_btn_handle():
            # “浏览文件”按钮槽函数
            if (
                self.item_table.currentRow() == -1
                or self.item_table.currentColumn() == 1
            ):
                # 用户未选中任何条目或选择的是DEST列，不做任何响应
                return

            self.data_browse_dlg.open()

        @Slot()
        def browse_dir_btn_handle():
            # “浏览文件夹”按钮槽函数
            if (
                self.item_table.currentRow() == -1
                or self.item_table.currentColumn() == 1
            ):
                # 用户未选中任何条目或选择的是DEST列，不做任何响应
                return

            self.data_dir_browse_dlg.open()

        @Slot(str)
        def browse_selected_handle(file_path: str):
            """
            处理文件对话框获取到用户打开文件/目录的槽函数 \n
            :param file_path: 用户打开的文件/目录路径
            """

            path = Path(file_path)
            current_row = self.item_table.currentRow()

            # SOURCE 列设置为操作系统绝对路径
            source_item = QTableWidgetItem(str(path.resolve()))
            source_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
            )
            self.item_table.setItem(current_row, 0, source_item)

            # DEST 列设置为表示顶层目录的"."或与入口脚本的相对路径
            dest_item = QTableWidgetItem(str(path.relative_to(self._work_dir)))
            # FIXME 处理相对路径错误
            if path.is_dir():
                self.item_table.setItem(current_row, 1, dest_item)
            else:
                self.item_table.setItem(current_row, 1, QTableWidgetItem("."))

        def ok_btn_handle():
            # “确定”按钮槽函数
            # TODO 删掉所有空白行
            self.data_selected.emit(self._submit())
            self.close()

        # noinspection DuplicatedCode
        self.new_btn.clicked.connect(new_btn_handle)
        self.delete_btn.clicked.connect(delete_btn_handle)
        self.browse_btn.clicked.connect(browse_btn_handle)
        self.browse_dir_btn.clicked.connect(browse_dir_btn_handle)
        self.data_browse_dlg.fileSelected.connect(browse_selected_handle)
        self.data_dir_browse_dlg.fileSelected.connect(browse_selected_handle)

        self.ok_btn.clicked.connect(ok_btn_handle)
        self.cancel_btn.clicked.connect(self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddDataWindow()
    window.show()
    sys.exit(app.exec())
