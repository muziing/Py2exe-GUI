# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""自实现 QObject.tr() 方法，使得 PyCharm 等静态检查工具不再报错。
"""

__all__ = [
    "QObjTr",
]

from typing import Optional

from PySide6.QtCore import QCoreApplication


class QObjTr:
    """利用 Python 多继承机制，为任何需要Qt翻译的类提供类方法 `tr()`。

    只能通过类名调用（形如 CLASSNAME.tr()），不能通过实例调用（形如 self.tr()）！对于有继承关系的控件，
    通过子类的实例调用 tr() 只能得到子类方法中涉及的字符串，而在父类中涉及的字符串都会丢失。

    假设有名为 MainWindow 的类，继承自 PySide6.QtWidgets.QMainWindow，需要在其实例属性中设置带翻译的文本，
    那么应当这样做：

    1. 将 MainWindow 同时继承自 QObjTr 和 QMainWindow：`class MainWindow(QObjTr, QMainWindow): ...`
    2. 在实例属性中，凡需要翻译的字符串，使用 MainWindow.tr()包裹，比如：`MainWindow.tr("&File")`
    """

    @classmethod
    def tr(cls, msg: str, disambiguation: Optional[str] = None, n: int = -1) -> str:
        """Returns a translated version of `msg`

        **Note: Can only be used as `CLASSNAME.tr()`, not as `self.tr()`!**

        **注意：只能通过类名调用，不能通过实例调用！否则会在涉及到继承的控件中失效。**

        Wrap `QCoreApplication.translate()` to `QObject.tr()`.This will make PyCharm
        happy. Now you can use `CLASSNAME.tr()` freely. For more details, see:
        <https://doc.qt.io/qt-6/qcoreapplication.html#translate>
        <https://doc.qt.io/qt-6/qobject.html#tr>

        :param msg: Origin messages
        :param disambiguation: Disambiguate identical text, see Qt Docs for details
        :param n: Handle plural forms, see Qt Docs for details
        :return: Translated messages
        """

        return QCoreApplication.translate(cls.__name__, msg, disambiguation, n)
