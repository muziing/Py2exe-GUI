# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import enum
import subprocess
from typing import NamedTuple


@enum.unique
class PyEnvType(enum.IntFlag):
    """
    Python 解释器（环境）类型，如系统解释器、venv 虚拟环境等 \n
    """

    system = enum.auto()  # 系统解释器
    venv = enum.auto()  # venv 虚拟环境  https://docs.python.org/3/library/venv.html
    poetry = enum.auto()  # Poetry 环境  https://python-poetry.org/
    conda = enum.auto()  # conda 环境  https://docs.conda.io/en/latest/


class PyEnv(NamedTuple):
    """
    Python 解释器（环境）数据类
    """

    type: PyEnvType
    executable_path: str


def get_pyenv_version(pyenv: PyEnv) -> str:
    """
    获取Python解释器的版本，以形如 "3.11.7" 的字符串形式返回 \n
    :param pyenv: Python环境
    :return: Version of the Python interpreter, such as "3.11.7".
    """

    cmd = [
        pyenv.executable_path,
        "-c",
        "import platform;print(platform.python_version(), end='')",
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    version = str(result.stdout, encoding="utf-8")
    return version
