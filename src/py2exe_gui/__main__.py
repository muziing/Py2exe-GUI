# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication

from .Constants import PyInstOpt
from .Core import Packaging, PackagingTask
from .Resources import COMPILED_RESOURCES  # noqa
from .Utilities import PyEnv, open_dir_in_explorer
from .Widgets import MainWindow, SubProcessDlg


class MainApp(MainWindow):
    """
    应用主程序 \n
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.current_pyenv: PyEnv
        self.packaging_task = PackagingTask(self)
        self.packager = Packaging(self)
        self.subprocess_dlg = SubProcessDlg(self)

        self._connect_slots()

        self.status_bar.showMessage("就绪")

    def _connect_slots(self) -> None:
        """
        连接各种信号与槽 \n
        """

        self._connect_pyenv_change()
        self._connect_run_pkg_btn_slot()
        self._connect_mul_btn_slot(self.subprocess_dlg)

        self.center_widget.option_selected.connect(self.packaging_task.handle_option)
        self.packaging_task.option_set.connect(self.packager.set_pyinstaller_args)
        self.packaging_task.option_set.connect(self.center_widget.handle_option_set)
        self.packaging_task.option_error.connect(self.center_widget.handle_option_error)
        self.packaging_task.ready_to_pack.connect(
            self.center_widget.handle_ready_to_pack
        )
        self.packager.args_settled.connect(
            lambda val: self.center_widget.pyinstaller_args_browser.enrich_args_text(
                val
            )
        )
        self.packager.subprocess.output.connect(self.subprocess_dlg.handle_output)

        # 用户关闭子进程对话框时中止打包进程
        self.subprocess_dlg.finished.connect(
            lambda: self.packager.subprocess.abort_process(2000)
        )

    def _connect_pyenv_change(self):
        """
        处理用户通过选择不同的 Python 解释器时的响应
        """

        @Slot()
        def on_pyenv_change() -> None:
            """
            处理用户通过选择不同的 Python 解释器时的响应
            """

            self.current_pyenv = self.center_widget.pyenv_combobox.currentData()
            self.packager.set_python_path(self.current_pyenv.exe_path)
            self.center_widget.hidden_import_dlg.pkg_browser_dlg.load_pkg_list(
                self.current_pyenv.installed_packages
            )

        on_pyenv_change()  # 显式调用一次，确保用户无任何操作时也能正确处理默认pyenv
        self.center_widget.pyenv_combobox.currentIndexChanged.connect(on_pyenv_change)

    def _connect_run_pkg_btn_slot(self):
        @Slot()
        def on_run_packaging_btn_clicked() -> None:
            """
            “运行打包”按钮的槽函数 \n
            """

            # 先显示对话框窗口，后运行子进程，确保调试信息/错误信息能被直观显示
            self.subprocess_dlg.show()
            self.packager.run_packaging_process()

        self.center_widget.run_packaging_btn.clicked.connect(
            on_run_packaging_btn_clicked
        )

    def _connect_mul_btn_slot(self, subprocess_dlg):
        @Slot()
        def on_multifunction_btn_clicked() -> None:
            """
            处理子进程窗口多功能按钮点击信号的槽 \n
            """

            btn_text = self.subprocess_dlg.multifunction_btn.text()
            if btn_text == "取消":
                self.packager.subprocess.abort_process()
                self.subprocess_dlg.close()
            elif btn_text == "打开输出位置":
                script_path = self.packaging_task.using_option[PyInstOpt.script_path]
                dist_path = script_path.parent / "dist"
                open_dir_in_explorer(dist_path)
            elif btn_text == "关闭":
                self.subprocess_dlg.close()

        # 连接信号与槽
        subprocess_dlg.multifunction_btn.clicked.connect(on_multifunction_btn_clicked)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        重写关闭事件，进行收尾清理 \n
        :param event: 关闭事件
        """

        # self.packager.subprocess.abort_process(3000)  # 不会访问到此行
        super().closeEvent(event)


def main() -> None:
    """
    应用程序主入口函数
    便于 Poetry 由此函数级入口构建启动脚本 \n
    """

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
