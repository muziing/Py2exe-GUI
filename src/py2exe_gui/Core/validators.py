# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块包含数个验证器类，用于验证用户输入是否有效

`FilePathValidator.validate_script()` 用于验证用户给定的路径是否为有效的 Python 脚本；
`FilePathValidator.validate_icon()` 用于验证用户给定的图标文件是否有效；
`InterpreterValidator.validate()` 用于验证用户给定的路径是否为有效的 Python 解释器可执行文件；
"""

__all__ = [
    "FilePathValidator",
    "InterpreterValidator",
]

import os
import subprocess
from pathlib import Path
from typing import Union

from ..Constants import RUNTIME_INFO, Platform


class FilePathValidator:
    """根据给定的路径验证文件的有效性"""

    @classmethod
    def validate_script(cls, script_path: Union[str, Path]) -> bool:
        """验证脚本路径是否有效

        :param script_path: 脚本路径
        :return:脚本路径是否有效
        """

        path = Path(script_path)

        # 文件是否存在
        if not path.exists() or not path.is_file():
            return False

        # 是否对文件有读取权限
        if not os.access(script_path, os.R_OK):
            return False

        return True

    @classmethod
    def validate_icon(cls, icon_path: Union[str, Path]) -> bool:
        """验证图标路径是否有效

        :param icon_path: 图标路径
        """

        path = Path(icon_path)

        if not path.exists() and path.is_file():
            return False

        # TODO 如果安装了可选依赖 Pillow，则进行更精确的判断和尝试转换图像格式
        if RUNTIME_INFO.platform == Platform.windows:
            return path.suffix == ".ico"
        elif RUNTIME_INFO.platform == Platform.macos:
            return path.suffix == ".icns"

        return True


class InterpreterValidator:
    """验证给定的可执行文件是否为有效的Python解释器"""

    @classmethod
    def validate(cls, path: Union[str, Path, os.PathLike[str]]) -> bool:
        """验证 `path` 是否指向有效的Python解释器

        :return: 是否有效
        """

        itp_path = Path(path).absolute()

        if not (
            itp_path.exists()  # 该路径存在
            and itp_path.is_file()  # 为文件
            and os.access(itp_path, os.X_OK)  # 可执行权限
        ):
            return False

        try:
            # 尝试将该文件作为Python解释器运行
            subprocess_args = [str(itp_path), "-c", "import sys"]
            subprocess.run(args=subprocess_args, timeout=0.3, check=True)
        except subprocess.SubprocessError:
            return False
        except OSError as e:
            print(f"对 {path} 启动 Python 解释器有效性验证子进程失败：{e}")
            return False
        else:
            return True


if __name__ == "__main__":
    print(InterpreterValidator.validate("/usr/bin/python"))
