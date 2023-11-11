![Py2exe-GUI Logo](docs/source/images/py2exe-gui_logo_big.png)

<h2 align="center">Easy-to-use Python GUI packaging tool</h2>

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
English | <a href="README_zh.md">简体中文</a>
</p>

## Introduction

Py2exe-GUI is an assist tool based on [PySide6](https://doc.qt.io/qtforpython/index.html), designed to provide a complete yet easy-to-use GUI for [PyInstaller](https://pyinstaller.org/).

![Screenshot of the interface](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)

It has the following features:

- All options of PyInstaller are supported.
- Call any local Python interpreter with the corresponding environment. No need for repeat installations.(Not realized yet)
- Cross-platform, supports Windows, Linux and macOS.

## How to use

> Note: Py2exe-GUI is still in the early development stage, the way of using it may change frequently, so please check this instruction frequently.

### Option A: Install with `pip`

First, install PyInstaller in the Python interpreter environment which to be packaged:

```shell
pip install pyinstaller==5.7.0
```

Then install Py2exe-GUI with `pip`:

```shell
pip install py2exe-gui
```

Run:

```shell
python -m py2exe_gui
```

### Option B: Run through source code

Clone repo:

```shell
git clone https://github.com/muziing/Py2exe-GUI.git
```

Install [Poetry](https://python-poetry.org/) and create a virtual environment:

```shell
poetry init
```

Install the dependencies:

```shell
poetry install
```

Run [Py2exe-GUI.py](src/Py2exe-GUI.py):

```shell
cd src
python  Py2exe-GUI.py
```

## Structure

All source code is in the [src/py2exe_gui](src/py2exe_gui) directory.

- [Constants](src/py2exe_gui/Constants)
- [Core](src/py2exe_gui/Core)
- [Resources](src/py2exe_gui/Resources)
- [Widgets](src/py2exe_gui/Widgets)

## License

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
