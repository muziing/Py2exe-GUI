import os
from pathlib import Path
from shutil import rmtree

src_dir_path = Path("../src")
dist_path = src_dir_path / Path("dist")
build_path = src_dir_path / Path("build")
spec_path_list = list(src_dir_path.glob("*.spec"))


def clear():
    rmtree(dist_path)
    rmtree(build_path)
    for spec_file in spec_path_list:
        os.remove(spec_file)


clear()
