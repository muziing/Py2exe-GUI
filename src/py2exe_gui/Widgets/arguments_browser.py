# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from typing import Optional

from PySide6.QtWidgets import QTextBrowser, QWidget


class ArgumentsBrowser(QTextBrowser):
    """
    针对命令行参数列表特别优化的文本浏览器
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super(ArgumentsBrowser, self).__init__(parent)

    def enrich_args_text(self, args_list: list[str]) -> None:
        """
        对参数进行一定高亮美化后显示 \n
        :param args_list: 参数列表
        """

        text: list[str] = []
        for arg in args_list:
            if arg.startswith("--") or arg.startswith("-"):
                text.append(f"<font color='blue'>{arg}</font>")
            else:
                text.append(arg)
        self.setText(str(text))
