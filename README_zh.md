![Py2exe-GUI Logo](docs/source/images/py2exe-gui_logo_big.png)

<h2 align="center">强大易用的 Python 图形界面打包工具</h2>

<p align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/muziing/Py2exe-GUI">
<img alt="Python Version" src="https://img.shields.io/pypi/pyversions/py2exe-gui">
<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/py2exe-gui"></a>
<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/py2exe-gui.svg?label=PyPI%20downloads"></a>
<a href="https://doc.qt.io/qtforpython/index.html"><img alt="PySide Version" src="https://img.shields.io/badge/PySide-6.6-blue"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="https://img.shields.io/badge/mypy-checked-blue"></a>
</p>
<p align="center">
<a href="README.md">English</a> | 简体中文
</p>

## 简介

Py2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html) 开发的辅助工具，旨在为 [PyInstaller](https://pyinstaller.org/) 提供完整易用的图形化界面，方便用户进行 Python 项目的打包。

![界面截图](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)

有如下特性：

- 完全图形化界面，易用
- 支持 PyInstaller 的全部选项
- （暂未实现）可以调用本地任一 Python 解释器与对应环境（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可），无需在每个待打包的解释器环境中重复安装
- 跨平台，支持 Windows、Linux、MacOS

## 如何使用

> 注意：Py2exe-GUI 尚处早期开发阶段，使用方式可能频繁变化，注意经常查阅此使用说明。

### 方式1：通过 `pip` 安装

首先在待打包的 Python 解释器环境中安装 PyInstaller:

```shell
pip install pyinstaller==5.7.0
```

然后通过 pip 安装 Py2exe-GUI：

```shell
pip install py2exe-gui
```

运行

```shell
python -m py2exe_gui  # 注意连字符为_
```

### 方式2：通过仓库源码运行

克隆仓库：

```shell
git clone https://github.com/muziing/Py2exe-GUI.git
```

安装 [Poetry](https://python-poetry.org/) 并创建虚拟环境

```shell
poetry init
```

安装依赖项：

```shell
poetry install
```

运行 src 目录下的 [Py2exe-GUI.py](src/Py2exe-GUI.py):

```shell
cd src
python  Py2exe-GUI.py
```

## 项目结构

所有源代码均在 [py2exe_gui](src/py2exe_gui) 目录下
- [Constants](src/py2exe_gui/Constants) 中为常量
- [Core](src/py2exe_gui/Core) 包用于执行打包
- [Resources](src/py2exe_gui/Resources) 包中为图标等静态资源
- [Widgets](src/py2exe_gui/Widgets) 包包含所有界面控件

## 开源许可

![GPLv3](docs/source/images/gplv3-127x51.png)

```text
Py2exe-GUI
Copyright (C) 2022-2023  muzing

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
