# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块主要包含用于在界面上预览显示 PyInstaller 命令选项的 `ArgumentsBrowser` 类
"""

__all__ = [
    "get_line_continuation",
    "ArgumentsBrowser",
]

from typing import Optional

from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QMenu, QTextBrowser, QWidget

from ..Constants import RUNTIME_INFO, Platform
from ..Utilities import QObjTr

# 一组适合浅色背景的颜色
colors = ["#FD6D5A", "#FEB40B", "#6DC354", "#994487", "#518CD8", "#443295"]


def get_line_continuation() -> str:
    """获取当前运行平台对应的命令行续行符

    :return: line continuation character
    """

    # 各平台的命令行续行符
    line_continuation_text = {"shell": "\\", "cmd": "^", "powershell": "`"}

    if Platform.windows == RUNTIME_INFO.platform:
        return line_continuation_text["powershell"]
    else:
        return line_continuation_text["shell"]


def wrap_font_tag(raw_text: str, color: str, **kwargs):
    """辅助函数，用于为字符添加<font>标签包裹，属性可通过可变关键字参数传入

    :param raw_text: 原始字符文本
    :param color: 颜色
    """

    attributes = [f"color='{color}'"]
    attributes.extend(f"{k}='{v}'" for k, v in kwargs.items())
    attributes_text = " ".join(attr for attr in attributes if attr)  # 筛选出非空的属性
    tag_attributes = " " + attributes_text + " " if attributes_text else ""
    return f"<font {tag_attributes}>{raw_text}</font>"


class ArgumentsBrowser(QObjTr, QTextBrowser):
    """针对命令行参数列表特别优化的文本浏览器"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        # 右键菜单
        self.context_menu = QMenu(self)
        copy_action = self.context_menu.addAction(ArgumentsBrowser.tr("Copy"))
        copy_action.triggered.connect(self._handle_copy_action)
        export_action = self.context_menu.addAction(ArgumentsBrowser.tr("Export"))
        export_action.triggered.connect(self._handle_export_action)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """重写右键菜单事件

        :param event: 事件
        """

        self.context_menu.exec(event.globalPos())

    def _handle_copy_action(self) -> None:
        """处理复制事件"""

        # TODO 实现复制到系统剪切板
        self.copy()

    def _handle_export_action(self) -> None:
        """处理导出事件"""

        # TODO 实现到处到 PowerShell/Bash 脚本
        pass

    def enrich_args_text(self, args_list: list[str]) -> None:
        """对参数进行一定高亮美化后显示

        :param args_list: 参数列表
        """

        # 不间断换行（续行）符
        line_continuation = get_line_continuation() + "<br>" + ("&nbsp;" * 4)

        # 首个参数一定为待打包的 Python 脚本名
        enriched_arg_texts: list[str] = [wrap_font_tag(args_list[0], color=colors[4])]

        for arg in args_list[1:]:
            if arg.startswith("--") or arg.startswith("-"):
                enriched_arg_texts.append(line_continuation)  # 添加换行，便于阅读与复制导出脚本
                enriched_arg_texts.append(wrap_font_tag(arg, color=colors[1]))
            else:
                enriched_arg_texts.append(arg)

        self.setText("pyinstaller " + " ".join(enriched_arg_texts))
