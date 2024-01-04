"""开发脚本，便于调用 PySide6 提供的各种工具程序
"""

import subprocess

from dev_scripts.path_constants import (
    COMPILED_RESOURCES,
    PROJECT_ROOT,
    RESOURCES_PATH,
    SRC_PKG_PATH,
    WIDGETS_PATH,
)


def compile_resources() -> int:
    """调用 RCC 工具编译静态资源

    :return: rcc 进程返回码
    """

    compiled_file_path = COMPILED_RESOURCES
    qrc_file_path = RESOURCES_PATH / "resources.qrc"
    cmd = [
        "pyside6-rcc",
        "-o",
        compiled_file_path,
        qrc_file_path,
    ]

    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
    except subprocess.SubprocessError as e:
        print(f"RCC 编译进程错误：{e}")
        raise e
    else:
        print(f"已完成静态资源文件编译，RCC 返回码：{result.returncode}。")
        return result.returncode


def gen_ts(lang: str = "zh_CN") -> int:
    """调用 lupdate 工具分析源码，生成 .ts 文本翻译文件

    :param lang: 目标翻译语言代码
    :return: lupdate 返回码
    """

    source = [*list(WIDGETS_PATH.glob("**/*.py")), SRC_PKG_PATH / "__main__.py"]
    target = RESOURCES_PATH / "i18n" / f"{lang.replace('-', '_')}.ts"
    cmd = ["pyside6-lupdate", *source, "-ts", target]

    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
    except subprocess.SubprocessError as e:
        print(f"lupdate 进程错误：{e}")
        raise
    else:
        print(f"已完成文本翻译文件生成，lupdate 返回码：{result.returncode}。")
        return result.returncode


def gen_qm(lang: str = "zh_CN") -> int:
    """调用 lrelease 工具编译.ts 文本翻译文件

    :param lang: 目标翻译语言代码
    :return: lrelease 返回码
    """

    source = RESOURCES_PATH / "i18n" / f"{lang.replace('-', '_')}.ts"
    target = RESOURCES_PATH / "i18n" / f"{lang.replace('-', '_')}.qm"
    cmd = ["pyside6-lrelease", source, "-qm", target]

    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
    except subprocess.SubprocessError as e:
        print(f"lrelease 进程错误：{e}")
        raise
    else:
        print(f"已完成文本翻译文件编译，lrelease 返回码：{result.returncode}。")
        return result.returncode


if __name__ == "__main__":
    # compile_resources()
    gen_ts("zh_CN")
    # gen_qm("zh_CN")
