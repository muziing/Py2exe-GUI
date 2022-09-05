import subprocess
from typing import List


class Packaging:
    """执行打包的核心"""

    def __init__(self):
        self._args: List[str] = ["pyinstaller"]

    def get_pyinstaller_args(self, arg: tuple[str, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并以正确的顺序添加至命令参数列表
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if arg_key == "script_path":
            self._args.insert(1, arg_value)
        elif arg_key == "icon_path":
            self._args.extend(["--icon", arg_value])

        print(self._args)  # 测试用

    def run_packaging_process(self) -> subprocess.CompletedProcess:
        """
        使用给定的参数启动打包子进程 \n
        :return: 子进程执行结果
        """

        try:
            run_result = subprocess.run(self._args, stdout=subprocess.PIPE)
            return run_result
        except Exception:
            print(Exception)
            # TODO 处理异常


if __name__ == "__main__":
    packager = Packaging()
    packager._args += ["-v"]
    print(packager.run_packaging_process())
