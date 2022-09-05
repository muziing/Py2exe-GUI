import subprocess
from typing import List


class Packaging:
    """执行打包的核心"""

    def __init__(self):
        self.full_args = {"script_path": "", "icon_path": "", "FD": ""}
        self._args: List[str] = ["pyinstaller"]

    def get_pyinstaller_args(self, arg: tuple[str, str]) -> None:
        """
        解析传递来的PyInstaller运行参数，并以正确的顺序添加至命令参数列表
        :param arg: 运行参数
        """

        arg_key, arg_value = arg
        if arg_key in self.full_args.keys():
            self.full_args[arg_key] = arg_value

    def set_pyinstaller_args(self) -> None:
        full_args = self.full_args
        self._args.extend([full_args["script_path"]])
        if full_args["icon_path"]:
            self._args.extend(["--icon", full_args["icon_path"]])
        if full_args["FD"]:
            if full_args["FD"] == "One Dir":
                self._args.extend(["--onedir"])
            elif full_args["FD"] == "One File":
                self._args.extend(["--onefile"])

        print(self._args)  # 测试用

    def run_packaging_process(self) -> subprocess.CompletedProcess:
        """
        使用给定的参数启动打包子进程 \n
        :return: 子进程执行结果
        """

        self._args = ["pyinstaller"]
        self.set_pyinstaller_args()
        return subprocess.run(["pyinstaller", "-v"])
        # try:
        #     run_result = subprocess.run(self._args, stdout=subprocess.PIPE)
        #     return run_result
        # except Exception:
        #     print(Exception)
        #     # TODO 处理异常


if __name__ == "__main__":
    packager = Packaging()
    packager._args += ["-v"]
    print(packager.run_packaging_process())
