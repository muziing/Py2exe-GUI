# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import os
import subprocess
from pathlib import Path
from typing import Union


class FilePathValidator:
    """
    根据给定的路径验证文件的有效性
    """

    @classmethod
    def validate_script(cls, script_path: Union[str, Path]) -> bool:
        """
        验证脚本路径是否有效 \n
        :param script_path: 脚本路径
        """

        path = Path(script_path)
        # TODO 完善验证方法
        return path.exists() and path.is_file()

    @classmethod
    def validate_icon(cls, icon_path: Union[str, Path]) -> bool:
        """
        验证图标路径是否有效 \n
        :param icon_path: 图标路径
        """

        path = Path(icon_path)
        # TODO 完善验证方法，根据 Windows(.ico)、macOS(.icns) 动态分析
        return path.exists() and path.is_file()


class InterpreterValidator:
    """
    验证给定的可执行文件是否为有效的Python解释器 \n
    """

    def __init__(self, path: Union[str, os.PathLike[str]]) -> None:
        """
        :param path: 可执行文件路径
        """

        self._itp_path: Path = Path(path)
        self._itp_validated: bool = False
        self.validate_itp()

    def validate_itp(self) -> bool:
        """
        :return: 解释器是否有效
        """

        if (
            self._itp_path.exists()  # 该路径存在
            and self._itp_path.is_file()  # 为文件
            and self._itp_path.name.startswith("python")  # 文件名以python起始
        ):
            try:
                # 尝试将该文件作为Python解释器运行
                subprocess_args = [
                    str(self._itp_path.resolve()),
                    "-c",
                    "import sys",
                ]
                result = subprocess.run(
                    args=subprocess_args,
                    timeout=300,
                )
                if result.returncode == 0:
                    self._itp_validated = True
                    return True
                else:
                    self._itp_validated = False
                    return False
            except OSError:
                self._itp_validated = False
                return False
        else:
            self._itp_validated = False
            return False

    @classmethod
    def validate(cls, path: Union[str, os.PathLike[str]]) -> bool:
        """
        验证path是否指向有效的Python解释器 \n
        :return: 是否有效
        """

        return InterpreterValidator(path).validate_itp()


if __name__ == "__main__":
    print(InterpreterValidator.validate("/usr/bin/python"))
