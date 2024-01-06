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
import warnings
from importlib import util as importlib_util
from pathlib import Path
from typing import Union

from ..Constants import RUNTIME_INFO, Platform


class FilePathValidator:
    """根据给定的路径验证文件的有效性"""

    @classmethod
    def validate_script(cls, script_path: Union[str, Path]) -> bool:
        """验证脚本路径是否有效

        :param script_path: 脚本路径
        :return: 脚本路径是否有效
        """

        path = Path(script_path)

        if not (path.exists() and path.is_file() and os.access(script_path, os.R_OK)):
            return False

        return True

    @classmethod
    def validate_icon(cls, icon_path: Union[str, Path]) -> bool:
        """验证图标路径是否有效

        :param icon_path: 图标路径
        :return: 图标是否有效
        """

        path = Path(icon_path)

        if not (path.exists() and path.is_file() and os.access(icon_path, os.R_OK)):
            return False

        if importlib_util.find_spec("PIL") is not None:
            # 如果安装了可选依赖 Pillow，则进行更精确的判断
            from PIL import Image, UnidentifiedImageError

            try:
                with Image.open(path) as img:
                    img_format: str = img.format
            except UnidentifiedImageError:
                return False
            else:
                if img_format is None:
                    return False
                elif RUNTIME_INFO.platform == Platform.windows:
                    return img_format == "ICO"
                elif RUNTIME_INFO.platform == Platform.macos:
                    return img_format == "ICNS"

        else:
            # 若未安装 Pillow，则简单地用文件扩展名判断
            if RUNTIME_INFO.platform == Platform.windows:
                return path.suffix == ".ico"
            elif RUNTIME_INFO.platform == Platform.macos:
                return path.suffix == ".icns"

        # 如果以上所有检查项均通过，默认返回 True
        return True


class InterpreterValidator:
    """验证给定的可执行文件是否为有效的Python解释器"""

    @classmethod
    def validate(cls, itp_path: Union[str, Path, os.PathLike[str]]) -> bool:
        """验证 `path` 是否指向有效的Python解释器

        :param itp_path: 文件路径
        :return: 是否有效
        """

        path = Path(itp_path).absolute()

        if not (path.exists() and path.is_file() and os.access(path, os.X_OK)):
            return False

        # 尝试将该文件作为Python解释器运行
        subprocess_args = [str(path), "-c", "import sys"]
        try:
            subprocess.run(args=subprocess_args, check=True)
        except subprocess.SubprocessError:
            return False
        except OSError as e:
            warnings.warn(
                f"Failed to start the Python interpreter validation subprocess for {path}: {e}",
                Warning,
                stacklevel=2,
            )
            return False
        else:
            return True
