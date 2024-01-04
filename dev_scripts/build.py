"""用于构建项目的脚本
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
from dev_scripts.path_constants import PROJECT_ROOT, README_FILE_LIST, SRC_PATH


def process_md_images(md_file_list: list[Path]) -> None:
    """处理 Markdown 文档中的图片链接

    在构建前替换为 GitHub 图床链接，在构建后替换回本地目录中的路径

    :param md_file_list: Markdown 文件列表
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


def export_requirements() -> int:
    """将项目依赖项导出至 requirements.txt 中

    :return: poetry export 命令返回值
    """

    poetry_export_cmd = [
        "poetry",
        "export",
        "--without-hashes",
        "-o",
        PROJECT_ROOT / "requirements.txt",
        "--format=requirements.txt",
    ]

    try:
        result = subprocess.run(poetry_export_cmd)
    except subprocess.SubprocessError as e:
        print(f"poetry export 进程错误：{e}")
        raise e
    else:
        print(f"已将当前项目依赖导出至 requirements.txt，poetry export 返回码：{result.returncode}")
        return result.returncode


def build_py2exe_gui() -> None:
    """构建项目的总函数"""

    if check_version_num() + check_license_statement() == 0:
        # 准备工作
        clear_pyinstaller_dist(SRC_PATH)
        clear_pycache(SRC_PATH)
        process_md_images(README_FILE_LIST)
        # compile_resources()
        export_requirements()
        print(f"pre-commit 检查完毕，返回码：{check_pre_commit()}。")
        print(f"mypy 检查完毕，返回码：{check_mypy()}。")

        # 正式构建
        try:
            result = subprocess.run(["poetry", "build"], check=True)
        except subprocess.SubprocessError as e:
            print(f"Poetry build 失败：{e}")
            raise
        else:
            print(f"Poetry build 完毕，返回码：{result.returncode}。")
        finally:
            # 清理
            process_md_images(README_FILE_LIST)
    else:
        print("有未通过的检查项，不进行构建")


if __name__ == "__main__":
    # process_md_images()
    # compile_resources()
    # export_requirements()
    build_py2exe_gui()
