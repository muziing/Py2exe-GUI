# Py2exe-GUI

Py2exe-GUI 是一个基于 PySide6 开发的 PyInstaller 辅助工具，旨在提供完整易用的图形化界面，方便用户使用 PyInstaller 进行 Python 项目的打包。

- 完全图形化界面，易用
- 支持 PyInstaller 的全部选项
- 可以调用本地任何一个 Python 解释器，无需在每个待打包的解释器环境中重复安装
- 跨平台，Windows、Linux、MacOS 均支持


## 项目结构

项目所有代码均在 [src](src) 目录下

[Widgets](src/Widgets) 下包含了所有需要的控件，main中使用多继承方式实现界面与功能相分离.

仅为图形化界面工具，不依赖于需要打包的Python环境。也提供exe发布版

可以显式指定打包时使用的 Python解释器与对应环境
（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可）

## TODO

 - [ ] 将参数拼接成完整调用命令
 - [ ] logging 日志记录
 - [ ] Python 解释器选择器
