# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""Py2exe-GUI 软件包入口

主要包含 `MainApp` 类，将前端界面和后端功能在此结合。
包含一个名为 `main()` 的入口函数
"""

import sys
from pathlib import Path

from PySide6.QtCore import QTranslator, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication

from .Constants import RUNTIME_INFO, PyInstOpt
from .Core import Packaging, PackagingTask
from .Resources import COMPILED_RESOURCES  # noqa
from .Utilities import open_dir_in_explorer
from .Widgets import MainWindow, SubProcessDlg


class MainApp(MainWindow):
    """应用主程序"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.packaging_task = PackagingTask(self)
        self.packager = Packaging(self)
        self.subprocess_dlg = SubProcessDlg(self)

        self._connect_slots()

        self.status_bar.showMessage(MainApp.tr("Ready."))

    # def show(self):
    #     """仅供分析启动性能使用，切勿取消注释！！！
    #     """
    #
    #     super().show()
    #     sys.exit()

    def _connect_slots(self) -> None:
        """连接各种信号与槽"""

        self._connect_run_pkg_btn_slot()
        self._connect_mul_btn_slot(self.subprocess_dlg)

        self.center_widget.option_selected.connect(self.packaging_task.on_opt_selected)
        self.packaging_task.option_set.connect(self.packager.set_pyinstaller_args)
        self.packaging_task.option_set.connect(self.center_widget.handle_option_set)
        self.packaging_task.option_error.connect(self.center_widget.handle_option_error)
        self.packaging_task.ready_to_pack.connect(
            self.center_widget.handle_ready_to_pack
        )
        self.packager.args_settled.connect(
            self.center_widget.pyinstaller_args_browser.enrich_args_text
        )
        self.packager.subprocess.output.connect(self.subprocess_dlg.handle_output)

        # 用户关闭子进程对话框时中止打包进程
        self.subprocess_dlg.finished.connect(
            lambda: self.packager.subprocess.abort_process(2000)
        )

    def _connect_run_pkg_btn_slot(self):
        @Slot()
        def handle_run_pkg_btn_clicked() -> None:
            """“运行打包”按钮的槽函数"""

            # 将当前选择的 Python 解释器作为打包使用的解释器
            current_pyenv = self.center_widget.pyenv_combobox.get_current_pyenv()
            self.packaging_task.pyenv = current_pyenv
            self.packager.set_python_path(current_pyenv.exe_path)

            # 先显示对话框窗口，后运行子进程，确保调试信息/错误信息能被直观显示
            self.subprocess_dlg.show()
            self.packager.run_packaging_process()

        self.center_widget.run_packaging_btn.clicked.connect(handle_run_pkg_btn_clicked)

    def _connect_mul_btn_slot(self, subprocess_dlg):
        @Slot()
        def handle_mul_btn_clicked() -> None:
            """处理子进程窗口多功能按钮点击信号的槽"""

            btn_text = self.subprocess_dlg.multifunction_btn.text()
            if btn_text == SubProcessDlg.tr("Cancel"):
                self.packager.subprocess.abort_process()
                self.subprocess_dlg.close()
            elif btn_text == SubProcessDlg.tr("Open Dist"):
                script_path: Path = self.packaging_task.using_option[
                    PyInstOpt.script_path
                ]
                dist_path = script_path.parent / "dist"
                open_dir_in_explorer(dist_path)
            elif btn_text == SubProcessDlg.tr("Close"):
                self.subprocess_dlg.close()

        subprocess_dlg.multifunction_btn.clicked.connect(handle_mul_btn_clicked)

    def closeEvent(self, event: QCloseEvent) -> None:
        """重写关闭事件，进行收尾清理

        :param event: 关闭事件
        """

        # self.packager.subprocess.abort_process(3000)  # 不会访问到此行
        super().closeEvent(event)


def main() -> None:
    """应用程序主入口函数，便于 Poetry 由此函数级入口构建启动脚本"""

    app = QApplication(sys.argv)

    # TODO 翻译机制待优化
    translator = QTranslator()
    if RUNTIME_INFO.language_code == "zh_CN":
        translator.load(":/i18n/zh_CN.qm")
    app.installTranslator(translator)

    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
