# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import enum


@enum.unique
class PyEnvType(enum.IntFlag):
    """
    Python 解释器（环境）类型，如系统解释器、venv 虚拟环境等 \n
    """

    system = enum.auto()  # 系统解释器
    venv = enum.auto()  # venv 虚拟环境  https://docs.python.org/3/library/venv.html
    poetry = enum.auto()  # Poetry 环境  https://python-poetry.org/
    conda = enum.auto()  # conda 环境  https://docs.conda.io/en/latest/
    unknown = enum.auto()  # 未知
