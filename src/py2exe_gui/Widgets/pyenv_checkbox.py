# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import platform
import sys
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox, QWidget

from ..Constants.python_env_constants import PyEnv, PyEnvType, get_pyenv_version


class PyEnvComboBox(QComboBox):
    """
    用于选择解释器环境的下拉框
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setIconSize(QSize(18, 18))

        self.addItem(
            QIcon(":/Icons/Python_128px"),
            f"Python {platform.python_version()}",
            sys.executable,
        )

        self.addItem(
            *self.gen_item(PyEnv(PyEnvType.poetry, executable_path=sys.executable))
        )

    @classmethod
    def gen_item(cls, pyenv: PyEnv) -> tuple:
        """
        根据传入的Python环境，生成一个适用于 QComboBox.addItem() 参数的三元素元组 \n
        :param pyenv: Python解释器环境
        :return: (icon, text, data)
        """

        data = pyenv.executable_path
        version = get_pyenv_version(pyenv)

        if pyenv.type == PyEnvType.system:
            icon = QIcon(":/Icons/Python_128px")
            text = f"Python {version}"
        elif pyenv.type == PyEnvType.poetry:
            icon = QIcon(":/Icons/Poetry")
            text = f"Poetry[Python {version}]"
        elif pyenv.type == PyEnvType.conda:
            icon = QIcon(":/Icons/Conda")
            text = f"Conda[Python {version}]"
        else:
            icon = QIcon(":/Icons/Python_128px")
            text = f"Python {version}"

        return icon, text, data
