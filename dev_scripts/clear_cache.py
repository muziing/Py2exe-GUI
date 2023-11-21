import os
from pathlib import Path
from shutil import rmtree

src_dir_path = Path("../src")


def clear_pyinstaller_dist(src_path: Path) -> None:
    """
    清理开发过程中测试运行时的打包中间文件及结果文件 \n
    :param src_path: Py2exe-GUI.py 运行目录
    """

    dist_path = src_path / Path("dist")
    build_path = src_path / Path("build")
    spec_path_list = list(src_path.glob("*.spec"))
    if dist_path.exists():
        rmtree(dist_path)
    if build_path.exists():
        rmtree(build_path)
    if spec_path_list:
        for spec_file in spec_path_list:
            os.remove(spec_file)
    print("Pyinstaller dist all cleaned.")


def clear_pycache(src_path: Path) -> None:
    """
    清理给定路径下的所有 .pyc .pyo 文件与 __pycache__ 目录 \n
    ref: https://stackoverflow.com/a/41386937
    :param src_path: 源码 src 目录路径
    """

    [p.unlink() for p in src_path.rglob("*.py[co]")]
    [p.rmdir() for p in src_path.rglob("__pycache__")]
    print("PyCache all cleaned.")


if __name__ == "__main__":
    clear_pyinstaller_dist(src_dir_path)
    clear_pycache(src_dir_path)