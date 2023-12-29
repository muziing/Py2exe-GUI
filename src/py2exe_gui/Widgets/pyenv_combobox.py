# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""本模块主要包含用于选择 Python 解释器环境的下拉框控件 `PyEnvComboBox`
"""

import sys
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox, QWidget

from ..Constants import RUNTIME_INFO, PyEnvType
from ..Utilities import PyEnv, get_sys_python


class PyEnvComboBox(QComboBox):
    """用于选择解释器环境的下拉框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        :param parent: 父控件对象
        """

        super().__init__(parent)

        self.setIconSize(QSize(18, 18))

        if not RUNTIME_INFO.is_bundled:
            # 在非 PyInstaller 捆绑环境中，第一项为当前用于运行 Py2exe-GUI 的 Python 环境
            current_pyenv = PyEnv(sys.executable, None)
            self.addItem(*self._gen_item(current_pyenv))
        else:
            # 若已由 PyInstaller 捆绑成冻结应用程序，则第一项为系统 Python 环境
            sys_pyenv = PyEnv(get_sys_python(), PyEnvType.system)
            self.addItem(*self._gen_item(sys_pyenv))

    @staticmethod
    def _gen_item(pyenv: PyEnv) -> tuple:
        """根据传入的 Python 环境，生成一个适用于 QComboBox.addItem() 参数的三元素元组

        :param pyenv: Python 解释器环境
        :return: (icon, text, data)
        :raise ValueError: PyEnv 类型无效时抛出
        """

        if not isinstance(pyenv.type, PyEnvType):
            raise ValueError(
                f'Current PyEnv type "{pyenv.type}" is not instance of "PyEnvType"'
            )

        data = pyenv
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

        icon = icon_map.get(pyenv.type, QIcon(":/Icons/Python_128px"))
        text = text_map.get(pyenv.type, f"Python {version}")

        return icon, text, data
