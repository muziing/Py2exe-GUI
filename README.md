![Py2exe-GUI Logo](docs/source/images/py2exe-gui_logo_big.png)

<h2 align="center">强大易用的 Python 图形界面打包工具</h2>

<p align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/muziing/Py2exe-GUI">
<img alt="Python Version" src="https://img.shields.io/pypi/pyversions/py2exe-gui">
<a href="https://pypi.org/project/py2exe-gui/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/py2exe-gui"></a>
<a href="https://doc.qt.io/qtforpython/index.html"><img alt="PySide Version" src="https://img.shields.io/badge/PySide-6.2-blue"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
</p>

## 简介

Py2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html) 开发的 [PyInstaller](https://pyinstaller.org/) 辅助工具，旨在提供完整易用的图形化界面，方便用户进行 Python 项目的打包。

![截图](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)

有如下特性：

- 完全图形化界面，易用
- 支持 PyInstaller 的全部选项
- （暂未实现）可以调用本地任一 Python 解释器，无需在每个待打包的解释器环境中重复安装
- 可以显式指定打包时使用的 Python 解释器与对应环境（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可）
- 跨平台，支持 Windows、Linux、MacOS

## 如何使用

> 注意：Py2exe-GUI 尚处早期开发阶段，使用方式可能频繁变化，注意经常查阅此使用说明。

### 方式1：通过 `pip` 安装

首先在待打包的 Python 解释器环境中安装 PyInstaller:

```shell
pip install pyinstaller==5.5
```

然后通过 pip 安装 Py2exe-GUI：

```shell
pip install py2exe-gui
```

运行

```shell
python -m py2exe_gui
```

### 方式2：通过仓库源码运行

克隆仓库：

```shell
git clone https://github.com/muziing/Py2exe-GUI.git
```

安装依赖项（需要提前安装好 [Poetry](https://python-poetry.org/)）：

```shell
poetry install
```

运行 src 目录下的 [Py2exe-GUI.py](src/Py2exe-GUI.py):

```shell
cd src
python  Py2exe-GUI.py
```


## 项目结构

- 项目所有代码均在 [py2exe_gui](src/py2exe_gui) 目录下
- [Widgets](src/py2exe_gui/Widgets) 包包含所有界面控件
- [Core](src/py2exe_gui/Core) 包用于执行打包
- [Constants](src/py2exe_gui/Constants) 中为常量

## TODO

- [x] 解决相对引用与作为包运行问题
- [x] 选项参数获取
  - [x] 将参数拼接成完整调用命令
  - [x] 参数预览器控件
  - [ ] 优化拼接代码
- [x] 调用 `PyInstaller` 子进程
  - [x] 使用 `QProcess` 替代 `subprocess` 以解决界面卡死问题
  - [x] 将子进程的输出与状态显示至单独的弹出窗口
  - [ ] 为 `SubProcessDlg` 增加多功能按钮
  - [ ] 优化子进程相关代码，增强异常处理
- [ ] 增加主界面功能控件
  - [ ] 资源文件添加框
  - [ ] Python 解释器选择器
  - [x] 增加状态栏信息
  - [ ] 「简洁模式」/「详尽模式」切换
- [ ] 菜单栏功能
  - [ ] `PyInstaller` 选项参数详解表格
  - [ ] 打包任务读写
- [ ] 实现跨平台功能
  - [x] 获取当前运行平台
  - [ ] 以合理方式保存至某种全局变量中
  - [ ] 定制各平台特有功能
- [ ] 打包任务
  - [x] 创建打包任务，保存所有选项
  - [ ] ~~定义文件并以适当格式存储（`json`）~~
  - [ ] 创建 [`.spec` 文件](https://pyinstaller.org/en/stable/spec-files.html)
  - [ ] `spec` 编辑器
- [ ] 使用qrc管理[静态资源](src/py2exe_gui/Resources)
- [ ] `logging` 日志记录
- [ ] QSS 与美化
- [ ] 动画效果
- [ ] 翻译与国际化
