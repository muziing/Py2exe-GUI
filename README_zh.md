![Py2exe-GUI Logo](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/py2exe-gui_logo_big.png)

<h2 align="center">强大易用的 Python 图形界面打包工具</h2>

<p align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/muziing/Py2exe-GUI">
<img alt="Python Version" src="https://img.shields.io/pypi/pyversions/py2exe-gui">
<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/py2exe-gui"></a>
<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/py2exe-gui.svg?label=PyPI%20downloads"></a>
</p>
<p align="center">
<a href="https://doc.qt.io/qtforpython/index.html"><img alt="PySide Version" src="https://img.shields.io/badge/PySide-6.6-blue"></a>
<a href="https://github.com/astral-sh/ruff"><img alt="Ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://mypy-lang.org/"><img alt="Checked with mypy" src="https://img.shields.io/badge/mypy-checked-blue"></a>
</p>
<p align="center">
<a href="README.md">English</a> | 简体中文
</p>

## 简介

Py2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html)
开发的辅助工具，旨在为 [PyInstaller](https://pyinstaller.org/) 提供完整易用的图形化界面，方便用户进行 Python 项目的打包。

![界面截图](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/Py2exe-GUI_v0.3.0_mainwindow_screenshot.png)

![界面截图](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/Py2exe-GUI_v0.2.0_screenshot.png)

有如下特性：

- 完全图形化界面，易用。
- 将会支持 PyInstaller 的全部选项。
- 可以调用本地任一 Python 解释器与对应环境，无需在每个待打包的解释器环境中重复安装。
- 跨平台，支持 Windows、Linux、MacOS。

## 如何安装

> 注意：Py2exe-GUI 尚处早期开发阶段，提供的分发版本均为*beta-测试版*。安装方式也可能频繁变化，注意经常查阅此使用说明。

### 方式1：通过 `pip` 安装

首先在待打包的 Python 解释器环境中安装 PyInstaller:

```shell
pip install pyinstaller  # 必须在你的项目环境中安装
```

然后通过 pip 安装 Py2exe-GUI：

```shell
pip install py2exe-gui  # 可以安装至任何环境
```

运行

```shell
py2exe-gui
```

如果以脚本形式运行失败，还可以尝试作为 Python 包运行：

```shell
python -m py2exe_gui  # 注意连字符为_
```

### 方式2：通过仓库源码运行

对于喜欢尝鲜或急需最新 bug 修复的用户，可以通过仓库源码运行：

1. 下载[最新 main 分支源码](https://codeload.github.com/muziing/Py2exe-GUI/zip/refs/heads/main)

2. 解压后进入目录，启动命令行/终端，创建并激活虚拟环境：

    ```shell
    python -m venv venv  # 创建虚拟环境（Windows）
    .\venv\Scripts\activate.ps1  # 激活虚拟环境（Windows PowerShell）
    ```

    ```shell
    python3 -m venv venv  # 创建虚拟环境（Linux/macOS）
    source venv/bin/activate  # 激活虚拟环境（Linux/macOS）
    ```

3. 安装依赖、运行程序：

    ```shell
    pip install -r requirements.txt  # 安装依赖项
    python ./src/Py2exe-GUI.py  # 运行
    ```

## 贡献

Py2exe-GUI 是一个自由的开源软件，欢迎任何人为其开发贡献力量。

如果你在使用时遇到任何问题（包括
bug、界面错别字等），或者提议新增实用功能，可以提交一个 [issue](https://github.com/muziing/Py2exe-GUI/issues/new)。

如果你有能力有想法贡献代码，欢迎提交 pull
request。请尽可能遵守原有的代码风格，并确保新增代码能通过[静态检查](dev_scripts/check_funcs.py)。

## 开源许可

![GPLv3](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/gplv3-127x51.png)

Py2exe-GUI 采用 GPLv3 开源许可证，详情请参见 [LICENSE](LICENSE) 文件。

但有一个例外：如果你的项目仅使用 Py2exe-GUI 作为打包工具，而最终发布的软件中并不包含 Py2exe-GUI 的源码或二进制文件，那么你的项目不会受到
GPLv3 的限制，仍可作为闭源商业软件发布。

```text
Py2exe-GUI
Copyright (C) 2022-2024  Muzing

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
