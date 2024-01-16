# 开发待办事项

此文档用于记录灵感，内容格式较为随意。其中的大部分功能将会逐渐实现，也有部分可能会被删去。

如果你对 Py2exe-GUI 的新功能有建议，欢迎[提交 issue](https://github.com/muziing/Py2exe-GUI/issues/new)。

## 控件

- [ ] PyInstaller 子进程窗口 `SubProcessDlg`
    - [x] 将子进程的输出与状态显示至单独的对话框
    - [x] 增加多功能按钮
    - [x] 关闭窗口时中断子进程、清除输出
    - [x] 处理不能正确显示子进程错误的问题（会被“打包完成”遮盖）
    - [ ] 增加「将输出导出到日志文件」功能
    - [ ] 增加简单高亮功能
- [x] 命令浏览器
    - [x] 显示将传递给 PyInstaller 的选项列表
    - [x] 高亮提示
    - [x] 以终端命令格式显示完整命令，并添加续行符
    - [ ] 导出为脚本功能，根据运行时平台导出 bash、PowerShell 等格式脚本
- [x] 添加资源文件窗口
    - [x] `--add-data`、 `--add-binary`
    - [x] `--paths`、`--hidden-import` 等可多次调用的选项
    - [x] 模仿 Windows “编辑环境变量” 窗口，左侧条目，右侧添加删除编辑等按钮
- [x] Python 解释器选择器
    - [x] 文件浏览对话框选择解释器可执行文件
    - [x] 处理解释器验证器返回结果，异常时弹出对话框要求用户自行检查确认
    - [x] 创建「解释器环境类」，保存解释器路径等信息
    - [x] ComboBox 中列出各解释器，将解释器环境保存在全局变量 ALL_PY_ENVs 中
    - [x] 识别 系统解释器/venv/Poetry/conda 等
    - [ ] 识别是否已安装 `PyInstaller`，未安装则提供「一键安装」
    - [ ] 右键菜单，可以将现有的环境 pin（固定），并保存到缓存文件中，后续启动时自动加载
- [ ] 用户自定义选项输入框
    - [ ] 允许用户自行输入选项，添加到选项列表中
- [x] ToolTip 提示，对应 PyInstaller 文档，提供完整帮助信息
- [x] `PyInstaller` 选项参数详解表格（界面细节待优化）
- [x] 主窗口状态栏显示软件版本
- [ ] 「一键调试」模式，自动选择 `--onedir`、`--console`、`--debug` 等利于调试的选项
- [ ] 用户设置窗口：若干个选项卡
    - [ ] 界面语言
    - [ ] PyInstaller 选项
    - [ ] 导入/导出选项
    - [ ] 插件（比如 Pillow 是否已安装、UPX 是否可用等）
- [ ] 简洁视图（仅包含常用选项）/详细视图（包含所有 PyInstaller 可用选项） 切换

## 打包

- [x] 选项参数获取
    - [x] 将参数拼接成完整调用命令
    - [x] 使用枚举值控制参数
    - [x] 优化拼接代码
- [x] 调用 `PyInstaller` 子进程
    - [x] 使用 Python 解释器直接运行命令，而不是 `PyInstaller.exe`
    - [x] 使用 `QProcess` 替代 `subprocess` 以解决界面卡死问题
    - [x] 优化子进程相关代码，增强异常处理
- [ ] 打包任务
    - [x] 创建打包任务，保存所有选项
    - [ ] 导出打包任务（json 或 yaml 格式）与加载打包任务（与 [*Auto-py-to-exe*](https://github.com/brentvollebregt/auto-py-to-exe) 兼容？）
    - [ ] [创建 `.spec` 文件](https://pyinstaller.org/en/stable/man/pyi-makespec.html)
- [ ] 创建新的虚拟环境
    - [ ] 已识别系统解释器（或其他可用解释器）的前提下，提供创建新的 venv 虚拟环境功能
    - [ ] 识别 `requirements.txt`，如找到，以此为依据安装第三方包
    - [ ] 如未找到有效的需求文件，则使用 [pipreqs](https://github.com/bndr/pipreqs) 分析生成

## 界面

- [x] 实现跨平台功能
    - [x] 获取当前运行平台，保存至全局变量 `RUNTIME_INFO.platform` 中
    - [x] 定制各平台特有功能
- [x] 使用 `qrc` 管理静态资源
- [x] 翻译与国际化
    - [x] Qt 提供的界面文本自动翻译
    - [x] 自实现的不同语言下功能差异，如“打开PyInstaller文档”指向不同的链接等

## 用户设置

- [ ] 在用户家目录中创建配置文件夹与配置文件（YAML 格式？），用于保存用户设置
- [ ] 设置条目：
    - [ ] 界面语言
    - [ ] 是否使用 `--clean` `-y` 选项（默认自动使用）
    - [ ] 脚本导出格式（默认与当前平台对应，如 Windows 则为 PowerShell）

## 应用程序级

- [x] 解决相对引用与作为包运行问题
- [ ] 缓存目录
    - [ ] (?) 将用户使用过的 Python 环境保存到缓存文件中存储，下次启动时自动加载
    - [ ] `logging` 日志记录 Py2exe-GUI 的运行过程

## 美化

- [ ] QSS 与美化
- [ ] 动画效果
- [ ] (?) 使用组件库

## 构建与分发

平台：

- [ ] Windows 发行版
    - [ ] 创建[版本资源文件](https://muzing.gitbook.io/pyinstaller-docs-zh-cn/usage#bu-huo-windows-ban-ben-shu-ju)
- [ ] Linux 发行版

分发方式：

- [x] PyPI
- [x] GitHub Releases
- [ ] Arch Linux AUR
- [ ] Ubuntu PPA

## 可选依赖

- [ ] 在 PyPI 上提供“完整版”的发行，包含以下所有可选依赖项
- [ ] “普通版”也要有能力检测用户是否已经安装了某个/些可选依赖项并能协同工作
- [ ] [Pillow](https://python-pillow.org/)
    - [ ] 更精确可靠的图标文件格式识别（根据图片二进制内容判断，而不只是文件扩展名）
    - [ ] 在主窗口工具栏提供图像格式转换功能，将其他格式转换为平台对应的图标格式
- [ ] [UPX](https://upx.github.io/)
    - [ ] [仅限 Windows 平台](https://muzing.gitbook.io/pyinstaller-docs-zh-cn/usage#shi-yong-upx)
    - [ ] 设法添加到运行时的环境变量 PATH 中
    - [ ] 或者，PyInstaller 命令中自动添加 `--upx-dir` 选项
