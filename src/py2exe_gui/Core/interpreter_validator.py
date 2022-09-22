import os
import subprocess
from pathlib import Path
from typing import Union


class InterpreterValidator:
    """
    验证给定的可执行文件是否为有效的Python解释器，并获取该解释器相关信息
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

    def itp_info(self):
        """
        返回解释器的相关信息 \n
        """

        # FIXME 完善此方法
        if self._itp_validated:
            pass

    def module_installed(self, module: str) -> bool:
        """
        验证该解释器环境中是否已安装某个模块 \n
        :param module: 模块名，要求为import语句中使用的名称
        :return: 未安装该模块或解释器无效时返回False
        """

        if self._itp_validated:
            subprocess_arg_list = [
                str(self._itp_path.resolve()),
                "-c",
                f"import {module}",
            ]
            result = subprocess.run(
                args=subprocess_arg_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )
            if result.returncode != 0 and b"ModuleNotFoundError" in result.stderr:
                return False
            else:
                return True
        else:
            return False

    @classmethod
    def validate(cls, path: Union[str, os.PathLike[str]]) -> bool:
        """
        验证path是否指向有效的Python解释器 \n
        :return: 是否有效
        """

        return InterpreterValidator(path).validate_itp()


if __name__ == "__main__":
    # print(InterpreterValidator.validate("/usr/bin/python"))
    iv = InterpreterValidator("/usr/bin/python")
    print(iv.module_installed("PySide6"))
    print(iv.module_installed("black"))
