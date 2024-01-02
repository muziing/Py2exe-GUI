# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""本模块主要包含用于选择 Python 解释器环境的下拉框控件 `PyEnvComboBox`
"""

__all__ = ["PyEnvComboBox"]

import sys
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox, QWidget

from ..Constants import RUNTIME_INFO, PyEnvType
from ..Utilities import ALL_PY_ENVs, PyEnv, get_sys_python


class PyEnvComboBox(QComboBox):
    """用于选择解释器环境的下拉框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setIconSize(QSize(18, 18))
        self.setMinimumHeight(24)  # 确保图标显示完整
        self._add_default_item()

    def _add_default_item(self) -> None:
        """添加默认解释器环境条目"""

        if not RUNTIME_INFO.is_bundled:
            # 在非 PyInstaller 捆绑环境中，第一项为当前用于运行 Py2exe-GUI 的 Python 环境
            default_pyenv = PyEnv(sys.executable, None)
        else:
            # 若已由 PyInstaller 捆绑成冻结应用程序，则第一项为系统 Python 环境
            default_pyenv = PyEnv(get_sys_python(), PyEnvType.system)

        ALL_PY_ENVs.append(default_pyenv)
        self.addItem(*self.gen_item(default_pyenv, 0))

    @staticmethod
    def gen_item(pyenv: PyEnv, index: int) -> tuple:
        """根据传入的 Python 环境，生成一个适用于 QComboBox.addItem() 参数的三元素元组

        :param pyenv: Python 解释器环境
        :param index: 该环境在全局变量 ALL_PY_ENVs 中的索引值
        :return: (icon, text, data)
        :raise ValueError: PyEnv 类型无效时抛出
        """

        if not isinstance(pyenv.type, PyEnvType):
            raise ValueError(
                f'Current PyEnv type "{pyenv.type}" is not instance of "PyEnvType"'
            )

        data = index
        version = pyenv.pyversion

        icon_map = {
            PyEnvType.system: QIcon(":/Icons/Python_128px"),
            PyEnvType.venv: QIcon(":/Icons/Python_cyan"),
            PyEnvType.poetry: QIcon(":/Icons/Poetry"),
            PyEnvType.conda: QIcon(":/Icons/Conda"),
            PyEnvType.unknown: QIcon(":/Icons/Python_128px"),
        }

        text_map = {
            PyEnvType.system: f"Python {version} (System)",
            PyEnvType.venv: f"Python {version} (venv)",
            PyEnvType.poetry: f"Poetry [Python {version}]",
            PyEnvType.conda: f"Conda [Python {version}]",
            PyEnvType.unknown: f"Python {version}",
        }
        # TODO 根据路径为环境命名，如 "Poetry (Py2exe-GUI) [Python 3.11.7]"

        icon = icon_map.get(pyenv.type, QIcon(":/Icons/Python_128px"))
        text = text_map.get(pyenv.type, f"Python {version}")

        return icon, text, data

    def get_current_pyenv(self) -> PyEnv:
        """通过当前选中的条目索引值，从全局变量 `ALL_PY_ENVs` 中获取对应的 Python 环境

        :return: 当前在下拉框中选定的 Python 环境
        """

        current_pyenv: PyEnv = ALL_PY_ENVs[self.currentData()]

        return current_pyenv
