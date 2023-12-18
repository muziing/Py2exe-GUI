"""
开发脚本中使用的相对路径常量
所有脚本应以项目根目录为工作目录运行
"""

from pathlib import Path

PROJECT_ROOT = Path("../")  # 项目根目录
SRC_PATH = PROJECT_ROOT / "src"  # 源码目录
SRC_PKG_PATH = SRC_PATH / "py2exe_gui"
RESOURCES_PATH = SRC_PKG_PATH / "Resources"  # 静态资源文件目录
COMPILED_RESOURCES = RESOURCES_PATH / "COMPILED_RESOURCES.py"  # 编译静态资源文件
README_FILE_LIST = [
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "README_zh.md",
]  # README 文件列表
