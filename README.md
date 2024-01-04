![Py2exe-GUI Logo](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/py2exe-gui_logo_big.png)

<h2 align="center">Easy-to-use Python GUI packaging tool</h2>

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
English | <a href="README_zh.md">简体中文</a>
</p>

## Introduction

Py2exe-GUI is an assist tool based on [PySide6](https://doc.qt.io/qtforpython/index.html), designed to provide a
complete yet easy-to-use GUI for [PyInstaller](https://pyinstaller.org/).

![Screenshot](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/Py2exe-GUI_v0.3.1_mainwindow_screenshot_en.png)

![Screenshot](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/Py2exe-GUI_v0.2.0_screenshot.png)

It has the following features:

- Fully graphical interface, easy to use.
- All options of PyInstaller will be supported.
- You can invoke any local Python interpreter with its corresponding environment, eliminating the need to reinstall it
  in each interpreter environment to be packaged.
- Cross-platform, supports Windows, Linux and macOS.

## How to install

> Note: Py2exe-GUI is still in the early stages of development, and the distributions provided are *beta versions*.
> Installation methods may change frequently, so be sure to check these instructions often.

### Option A: Install with `pip`

First, install PyInstaller in the Python interpreter environment which to be packaged:

```shell
pip install pyinstaller  # Must be installed in your project environment
```

Then install Py2exe-GUI with `pip`:

```shell
pip install py2exe-gui  # Can be installed into any environment
```

Run:

```shell
py2exe-gui
```

You can run py2exe-gui as a package if running it as a script doesn't work:

```shell
python -m py2exe_gui  # `_`, not `-`
```

### Option B: Run through source code

For those who like to try it out or are in desperate need of the latest bug fixes, you can run it through the repository
source code:

1. Download the [latest main branching source code](https://codeload.github.com/muziing/Py2exe-GUI/zip/refs/heads/main).

2. Unzip it and go to the directory. Launch a terminal to create and activate the virtual environment:

    ```shell
    python -m venv venv  # create a virtual environment (Windows)
    .\venv\Scripts\activate.ps1  # and activate it (Windows, PowerShell)
    ```

    ```shell
    python3 -m venv venv  # create a virtual environment (Linux/macOS)
    source venv/bin/activate  # and activate it (Linux/macOS)
    ```

3. Install dependencies and run the program.

    ```shell
    pip install -r requirements.txt
    python ./src/Py2exe-GUI.py
    ```

## Contributing

Py2exe-GUI is a free and open source software and anyone is welcome to contribute to its development.

If you encounter any problems while using it (including
bugs, typos, etc.), or if you have suggestions for new features, you can open
an [issue](https://github.com/muziing/Py2exe-GUI/issues/new).

If you are able to contribute code, feel free to submit a pull-request.
Please follow the original code style as much as possible, and make sure that the new code passes all
the [checks](dev_scripts/check_funcs.py).

## License

![GPLv3](https://raw.githubusercontent.com/muziing/Py2exe-GUI/main/docs/source/images/gplv3-127x51.png)

Py2exe-GUI is licensed under the GPLv3 open source license, see the [LICENSE](LICENSE) file for details.

There is one exception: if your project uses Py2exe-GUI only as a packaging tool, and your final distribution does not
contain Py2exe-GUI's source code or binaries, then your project is not restricted by the GPLv3 restrictions and can
still be distributed as closed-source commercial software.

```text
Py2exe-GUI
Copyright (C) 2022-2024  muzing

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
