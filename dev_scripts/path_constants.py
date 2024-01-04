"""开发脚本中使用的相对路径常量

所有脚本应以项目根目录为工作目录运行
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent  # 项目根目录
SRC_PATH = PROJECT_ROOT / "src"  # 源码目录
SRC_PKG_PATH = SRC_PATH / "py2exe_gui"  # 包目录
RESOURCES_PATH = SRC_PKG_PATH / "Resources"  # 静态资源文件目录
COMPILED_RESOURCES = RESOURCES_PATH / "COMPILED_RESOURCES.py"  # 编译静态资源文件
WIDGETS_PATH = SRC_PKG_PATH / "Widgets"  # 控件目录
README_FILE_LIST = [
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "README_zh.md",
]  # README 文件列表
