# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import json
import subprocess
from pathlib import Path
from typing import Optional, Union

from ..Constants import PyEnvType


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
        self._executable_path = Path(executable_path)
        self.exe_path = str(executable_path)
        self.type = type_

        if type_ is None:
            # type_ 为 None 表示特殊含义——待推断
            self.type_ = self.infer_type(self._executable_path)

        self.pyversion = self.get_py_version(self._executable_path)
        self.installed_packages = self.get_installed_packages(self._executable_path)

    @staticmethod
    def get_py_version(executable_path: Union[str, Path]) -> str:
        """
        获取Python解释器的版本，以形如 "3.11.7" 的字符串形式返回 \n
        :return: Version of the Python interpreter, such as "3.11.7".
        """

        cmd = [
            f"{executable_path}",
            "-c",
            "import platform;print(platform.python_version(), end='')",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            version = result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get Python version: {e.output}") from e
        return version

    @staticmethod
    def get_installed_packages(executable_path: Union[str, Path]) -> list[dict]:
        """
        获取该 Python 环境中已安装的包信息 \n
        :param executable_path: Python 解释器可执行文件路径
        :return: 包列表，形如 [{'name': 'aiohttp', 'version': '3.9.1'}, {'name': 'aiosignal', 'version': '1.3.1'}, ...]
        """

        cmd = [
            f"{executable_path}",
            "-m",
            "pip",
            "list",
            "--format",
            "json",
            "--disable-pip-version-check",
            "--no-color",
            "--no-python-version-warning",
        ]

        try:
            # 运行 pip list 命令，获取输出
            result = subprocess.run(cmd, capture_output=True, text=True)
            pip_list = result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get installed packages: {e.output}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}") from e

        try:
            # json 解析
            installed_packages: list[dict] = json.loads(pip_list)
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse installed packages: {e}") from e

        return installed_packages

    @classmethod
    def infer_type(cls, executable_path: Union[str, Path]) -> PyEnvType:
        """
        推断 Python 环境类型，如 venv Poetry Conda 等 \n
        """

        pass

    def pkg_installed(self, package_name: str) -> bool:
        """
        检查特定软件包是否已安装 \n
        :param package_name: 待检索的软件包名称
        :return: 是否已安装
        """

        return any(pkg["name"] == package_name for pkg in self.installed_packages)


if __name__ == "__main__":
    test_env = PyEnv("/usr/bin/python")
    print(test_env.pyversion)
    # print(test_env.installed_packages)
    print(test_env.pkg_installed("yaml"))
