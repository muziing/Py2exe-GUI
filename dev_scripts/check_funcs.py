"""
各类检查函数
"""

import subprocess
import tomllib
import warnings

from dev_scripts.path_constants import COMPILED_RESOURCES, PROJECT_ROOT, SRC_PATH
from py2exe_gui import Constants as py2exe_gui_Constants


def check_license_statement() -> int:
    """
    检查源代码文件中是否都包含了许可声明
    :return: 0-所有源文件都包含许可声明；1-存在缺失许可声明的源文件
    """

    license_statement = "# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html\n"
    source_file_list = list(SRC_PATH.glob("**/*.py"))
    source_file_list.remove(COMPILED_RESOURCES)  # 排除RCC编译工具自动生成的.py文件
    check_pass = 0

    print("开始检查源码中许可声明情况...")

    for file in source_file_list:
        with open(file, encoding="utf-8") as f:
            if license_statement not in f.read():
                warning_mes = f"Source code file {file} lacks a license statement."
                warnings.warn(warning_mes, stacklevel=1)
            else:
                check_pass += 1

    if check_pass == len(source_file_list):
        print("许可声明检查完毕，所有源码文件都包含许可声明。")
        return 0
    else:
        print("许可声明检查完毕，部分源码文件缺失许可声明，请检查。")
        return 1


def check_version_num() -> int:
    """
    检查各部分声明的版本号是否一致 \n
    :return: 0-各处版本一致；1-存在版本不一致情况
    """

    print("正在检查各处版本号是否一致...")

    app_constant_version = py2exe_gui_Constants.app_constants.AppConstant.VERSION
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as ppj_toml_file:
        ppj_dict = tomllib.load(ppj_toml_file)
        ppj_version = ppj_dict["tool"]["poetry"]["version"]

    if ppj_version == app_constant_version:
        print(f"版本号检查完毕，均为 {ppj_version}。")
        return 0
    else:
        warning_mes = (
            """版本号不一致！\n"""
            + f"""pyproject.toml................{ppj_version}\n"""
            + f"""Constants.AppConstant.........{app_constant_version}\n"""
        )
        warnings.warn(warning_mes, stacklevel=1)
        return 1


def check_pre_commit() -> int:
    """
    调用已有的 pre-commit 检查工具进行检查 \n
    :return: pre-commit 进程返回码
    """

    pre_commit_run_cmd = ["pre-commit", "run", "--all-files"]
    print("开始进行第一次 pre-commit 检查...")
    result_1 = subprocess.run(pre_commit_run_cmd)
    if result_1.returncode != 0:
        print("开始进行第二次 pre-commit 检查...")
        result_2 = subprocess.run(pre_commit_run_cmd)
        if result_2.returncode != 0:
            warnings.warn("pre-commit进程返回码非0，建议检查", stacklevel=1)
        return result_2.returncode
    else:
        print("pre-commit 检查完成，所有项目通过。")
        return 0


def check_requirements() -> int:
    """
    检查 requirements.txt 中的依赖是否最新
    """

    pass


if __name__ == "__main__":
    check_license_statement()
    check_version_num()
    check_pre_commit()
    check_requirements()
