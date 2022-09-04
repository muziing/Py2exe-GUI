import pathlib
import subprocess
from typing import List


def run_packaging_process(args: List[str]) -> subprocess.CompletedProcess:
    """
    使用给定的参数启动打包子进程 \n
    :param args: 命令行参数
    :return: 子进程执行结果
    """
    arg = ["pyinstaller"]
    run_result = subprocess.run(args=arg + args, stdout=subprocess.PIPE)
    return run_result


if __name__ == "__main__":
    print(run_packaging_process(["pyinstaller", "-v"]))
