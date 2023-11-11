# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from typing import Optional

from PySide6.QtWidgets import QTextBrowser, QWidget

# 一组适合浅色背景的颜色
colors = ["#FD6D5A", "#FEB40B", "#6DC354", "#994487", "#518CD8", "#443295"]


def wrap_font_tag(raw_text: str, color: str, **kwargs):
    """
    辅助函数，用于为字符添加<font>标签包裹，属性可通过可变关键字参数传入 \n
    :param raw_text: 原始字符文本
    :param color: 颜色
    """

    attributes = f" color='{color}'"
    for k, v in kwargs.items():
        attributes += f" {k}={v}"
    return f"<font {attributes}>{raw_text}</font>"


class ArgumentsBrowser(QTextBrowser):
    """
    针对命令行参数列表特别优化的文本浏览器
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

    def enrich_args_text(self, args_list: list[str]) -> None:
        """
        对参数进行一定高亮美化后显示 \n
        :param args_list: 参数列表
        """

        text: list[str] = [wrap_font_tag(args_list[0], colors[4])]
        for arg in args_list[1:]:
            if arg.startswith("--") or arg.startswith("-"):
                text.append(wrap_font_tag(arg, colors[1]))
            else:
                text.append(arg)

        self.setText(str(text))
