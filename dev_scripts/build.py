"""用于构建项目的脚本
"""

import subprocess

from dev_scripts.check_funcs import (
    check_license_statement,
    check_mypy,
    check_pre_commit,
    check_version_num,
)
from dev_scripts.clear_cache import clear_pycache, clear_pyinstaller_dist
from dev_scripts.path_constants import PROJECT_ROOT, SRC_PATH


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
            pass
    else:
        print("有未通过的检查项，不进行构建")


if __name__ == "__main__":
    # export_requirements()
    build_py2exe_gui()
