# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import json
import subprocess
from pathlib import Path
from typing import Optional, Union

from Constants import PyEnvType


class PyEnv:
    """
    Python 解释器环境类，存储某个 Python 解释器对应的环境中的各种信息，如
    解释器可执行文件路径、Python 版本、已安装的包等 \n
    """

    def __init__(
        self,
        executable_path: Union[str, Path],
        type_: Optional[PyEnvType] = PyEnvType.unknown,
    ):
        self.executable_path = Path(executable_path)

        if type_ is None:
            # type_ 为 None 表示特殊含义——待推断
            self.type_ = self.infer_type(self.executable_path)

        self.pyversion = self.get_py_version(self.executable_path)
        self.installed_packages = self.get_installed_packages(self.executable_path)

    @classmethod
    def get_py_version(cls, executable_path: Union[str, Path]) -> str:
        """
        获取Python解释器的版本，以形如 "3.11.7" 的字符串形式返回 \n
        :return: Version of the Python interpreter, such as "3.11.7".
        """

        cmd = f"{executable_path} -c \"import platform;print(platform.python_version(), end='')\""
        version = subprocess.getoutput(cmd, encoding="utf-8")
        return version

    @classmethod
    def get_installed_packages(cls, executable_path: Union[str, Path]) -> list[dict]:
        """
        获取该 Python 环境中已安装的包信息 \n
        :param executable_path: Python 解释器可执行文件路径
        :return: 包列表，形如 [{'name': 'aiohttp', 'version': '3.9.1'}, {'name': 'aiosignal', 'version': '1.3.1'}, ...]
        """

        cmd = f"{executable_path} -m pip list --format json"
        pip_list = subprocess.getoutput(cmd)
        installed_packages: list[dict] = json.loads(pip_list)
        return installed_packages

    @classmethod
    def infer_type(cls, executable_path: Union[str, Path]) -> PyEnvType:
        """
        推断 Python 环境类型，如 venv Poetry Conda 等
        """

        pass

    def pkg_installed(self, package_name: str) -> bool:
        """
        检索某个包是否已安装
        :param package_name: 待检索的包名
        :return: 是否已安装
        """

        for package in self.installed_packages:
            if package["name"] == package_name:
                return True
        else:
            return False


if __name__ == "__main__":
    test_env = PyEnv("/usr/bin/python")
    print(test_env.pyversion)
    # print(test_env.installed_packages)
    print(test_env.pkg_installed("yaml"))
