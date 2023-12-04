"""
用于构建项目的脚本
"""

import subprocess
import tomllib
import warnings
from pathlib import Path

from dev_scripts.clear_cache import clear_pycache, clear_pyinstaller_dist
from py2exe_gui import Constants

project_root = Path("../")  # 项目根目录
src_path = project_root / "src"  # 源码目录
resources_path = src_path / "py2exe_gui" / "Resources"  # 静态资源文件目录
readme_file_list = [project_root / "README.md", project_root / "README_zh.md"]


# TODO 加入日志模块，保存构建日志


def process_md_images(md_file_list: list[Path]) -> None:
    """
    处理 Markdown 文档中的图片链接 \n
    在构建前替换为 GitHub 图床链接，在构建后替换回本地目录中的路径 \n
    :return: 处理方向，0-处置至本地路径，1-处理至GitHub路径
    """

    md_uri = "docs/source/images/"
    github_uri = (
        "https://github.com/muziing/Py2exe-GUI/raw/main"
        + "/docs/source/images/"
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


def check_version_num() -> bool:
    """
    检查各部分声明的版本号是否一致 \n
    """

    print("正在检查各处版本号是否一致...")

    app_constant_version = Constants.app_constants.AppConstant.VERSION
    with open(project_root / "pyproject.toml", "rb") as ppj_toml_file:
        ppj_dict = tomllib.load(ppj_toml_file)
        ppj_version = ppj_dict["tool"]["poetry"]["version"]

    if ppj_version == app_constant_version:
        print(f"版本号检查完毕，均为 {ppj_version} 。")
        return True
    else:
        warning_mes = (
            """版本号不一致！\n"""
            + f"""pyproject.toml................{ppj_version}\n"""
            + f"""Constants.AppConstant.........{app_constant_version}\n"""
        )
        warnings.warn(warning_mes, stacklevel=1)
        return False


def pre_commit_check() -> int:
    """
    调用已有的 pre-commit 检查工具进行检查 \n
    :return: pre-commit 进程返回码
    """

    pre_commit_run_cmd = ["pre-commit", "run", "--all-files"]
    print("开始进行第一次 pre-commit 检查：")
    result_1 = subprocess.run(pre_commit_run_cmd)
    if result_1.returncode != 0:
        print("开始进行第二次 pre-commit 检查：")
        result_2 = subprocess.run(pre_commit_run_cmd)
        if result_2.returncode != 0:
            warnings.warn("pre-commit进程返回码非0，建议检查", stacklevel=1)
        return result_2.returncode
    else:
        return 0


def compile_resources() -> int:
    """
    调用 RCC 工具编译静态资源 \n
    :return: rcc 进程返回码
    """

    compiled_file_path = resources_path / "compiled_resources.py"
    qrc_file_path = resources_path / "resources.qrc"
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

    if check_version_num():
        # 准备工作
        clear_pyinstaller_dist(src_path)
        clear_pycache(src_path)
        process_md_images(readme_file_list)
        # compile_resources()
        print(f"pre-commit检查完毕，返回码：{pre_commit_check()}。")

        # 正式构建
        subprocess.run(["poetry", "build"])  # TODO 处理异常与返回值

        # 清理
        process_md_images(readme_file_list)
    else:
        print("构建失败，有未通过的检查项")


if __name__ == "__main__":
    # check_version_num()
    # print(pre_commit_check())
    # compile_resources()
    # process_md_images()
    build_py2exe_gui()
