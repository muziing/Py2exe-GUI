"""
用于构建项目的脚本
"""

import subprocess
from pathlib import Path

from dev_scripts.check_funcs import (
    check_license_statement,
    check_mypy,
    check_pre_commit,
    check_version_num,
)
from dev_scripts.clear_cache import clear_pycache, clear_pyinstaller_dist
from dev_scripts.path_constants import README_FILE_LIST, RESOURCES_PATH, SRC_PATH

# TODO 加入日志模块，保存构建日志


def process_md_images(md_file_list: list[Path]) -> None:
    """
    处理 Markdown 文档中的图片链接 \n
    在构建前替换为 GitHub 图床链接，在构建后替换回本地目录中的路径 \n
    :return: 处理方向，0-处置至本地路径，1-处理至GitHub路径
    """

    md_uri = "docs/source/images/"
    github_uri = (
        "https://github.com/muziing/Py2exe-GUI/raw/main" + "/docs/source/images/"
    )

    for md_file in md_file_list:
        with open(md_file, "r+", encoding="UTF-8") as f:
            all_text = f.read()
            if github_uri not in all_text:
                print(f"将 {md_file} 中的本地图片路径替换为GitHub在线路径")
                all_text_new = all_text.replace(md_uri, github_uri)
            else:
                print(f"将 {md_file} 中的GitHub在线路径替换为本地图片路径")
                all_text_new = all_text.replace(github_uri, md_uri)
            f.seek(0)
            f.write(all_text_new)
            # FIXME 会在文件尾部多出来莫名其妙的行


def compile_resources() -> int:
    """
    调用 RCC 工具编译静态资源 \n
    :return: rcc 进程返回码
    """

    compiled_file_path = RESOURCES_PATH / "compiled_resources.py"
    qrc_file_path = RESOURCES_PATH / "resources.qrc"
    cmd = [
        "pyside6-rcc",
        "-o",
        str(compiled_file_path.resolve()),
        str(qrc_file_path.resolve()),
    ]
    result = subprocess.run(cmd)
    print(f"已完成静态资源文件编译，RCC返回码：{result.returncode}。")
    return result.returncode


def build_py2exe_gui() -> None:
    """
    构建项目的总函数 \n
    """

    if check_version_num() + check_license_statement() == 0:
        # 准备工作
        clear_pyinstaller_dist(SRC_PATH)
        clear_pycache(SRC_PATH)
        process_md_images(README_FILE_LIST)
        # compile_resources()
        print(f"pre-commit 检查完毕，返回码：{check_pre_commit()}。")
        print(f"mypy 检查完毕，返回码：{check_mypy()}。")

        # 正式构建
        subprocess.run(["poetry", "build"])  # TODO 处理异常与返回值

        # 清理
        process_md_images(README_FILE_LIST)
    else:
        print("构建失败，有未通过的检查项")


if __name__ == "__main__":
    # compile_resources()
    # process_md_images()
    build_py2exe_gui()
