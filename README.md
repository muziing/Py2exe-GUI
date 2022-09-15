# Py2exe-GUI

更易用的 Python 打包工具！

![GitHub Repo stars](https://img.shields.io/github/stars/muziing/Py2exe-GUI)
[![PyPI Version](https://img.shields.io/pypi/v/py2exe-gui)](https://pypi.org/project/py2exe-gui/)
[![License](https://img.shields.io/github/license/muziing/Py2exe-GUI)](https://www.gnu.org/licenses/gpl-3.0.html)
![Python version](https://img.shields.io/pypi/pyversions/py2exe-gui)
[![PySide Version](https://img.shields.io/badge/PySide-6.2-blue)](https://doc.qt.io/qtforpython/index.html)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## 简介

Py2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html) 开发的 [PyInstaller](https://pyinstaller.org/) 辅助工具，旨在提供完整易用的图形化界面，方便用户进行 Python 项目的打包。

![截图](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)

有如下特性：

- 完全图形化界面，易用
- 支持 PyInstaller 的全部选项
- 可以调用本地任何一个 Python 解释器，无需在每个待打包的解释器环境中重复安装（暂未实现）
- 跨平台，Windows、Linux、MacOS 均支持

## 如何使用

### 安装

Py2exe-GUI 已经发布至 PyPI，直接通过 pip 工具安装即可：

```shell
pip install py2exe-gui
```

### 运行

```shell
python -m py2exe_gui
```

## 项目结构

- 项目所有代码均在 [py2exe_gui](src/py2exe_gui) 目录下
- [Widgets](src/py2exe_gui/Widgets) 目录下包含所有界面控件
- [Core](src/py2exe_gui/Core) 目录中为执行打包的代码

仅为图形化界面工具，不依赖于需要打包的 Python 环境。也提供 exe 发布版。

可以显式指定打包时使用的 Python 解释器与对应环境
（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可）

## TODO

- [x] 解决相对引用问题
- [x] 将参数拼接成完整调用命令（完成待优化）
- [x] 使用 QProcess 替代 subprocess 以解决界面卡死问题
- [ ] 将 PyInstaller 的输出显示至单独的弹出窗口
- [ ] 子进程运行时阻塞主窗口关闭
- [ ] 增加状态栏信息
- [ ] Python 解释器选择器
- [ ] 实现跨平台功能（不同平台间的差异功能）
- [ ] 保存与读取打包项目文件（json? yaml? toml?）
- [ ] logging 日志记录
- [ ] QSS 与美化
- [ ] 翻译与国际化
