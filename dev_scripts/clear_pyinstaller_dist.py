"""
清理开发过程中测试运行时的打包中间文件及结果文件
"""

import os
from pathlib import Path
from shutil import rmtree

src_dir_path = Path("../src")
dist_path = src_dir_path / Path("dist")
build_path = src_dir_path / Path("build")
spec_path_list = list(src_dir_path.glob("*.spec"))


def clear():
    if dist_path.exists():
        rmtree(dist_path)
    if build_path.exists():
        rmtree(build_path)
    if spec_path_list:
        for spec_file in spec_path_list:
            os.remove(spec_file)
    print("All cleaned.")


clear()
