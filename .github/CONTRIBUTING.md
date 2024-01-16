# Contributing

> 简体中文版本在本文档下方。

Thank you very much for your willingness to contribute to the Py2exe-GUI project, please read the following and follow
some ground rules in order to keep the project in good shape for rapid development.

## Before Writing Code

If you have any thoughts that involve more than a few dozen lines of code, I highly recommend you to submit an issue first talking about the stuff you want to implement. It's a good idea to discuss whether we want to do it before you put a lot of effort into it, and it also ensures that we're not duplicating work.

## Coding

### Prepare the development environment

Development environment is more complicated than use environment, ensure that you have installed Python 3.11+ and [Poetry](https://python-poetry.org/docs/#installation). Then use Poetry to create and install the development environment:

```shell
cd Py2exe-GUI
poetry init
poetry install
```

You also need to install a git hook via [pre-commit](https://pre-commit.com/):

```shell
pre-commit install
```

### Code Style

- In general, new and modified code should be close to the style of the original code. Try to make the code readable.
- Please format the code using [Black](https://black.readthedocs.io/en/stable/) to ensure that all code styles are consistent with the project.
- Please add sufficient type annotations to the code for your code. This allows the code to pass [mypy](https://mypy.readthedocs.io/en/stable/) checks without reporting errors.
- Please add docstrings or comments to modules, classes, functions/methods, properties, etc. to ensure clarity and readability.

### Documentation

If you implement some new features, you should consider adding the appropriate documentation to the `docs/` directory, or modifying `README.md` as appropriate to elaborate.

### Tests

The Py2exe-GUI project does not have any tests at the moment due to my limited programming skills as well as the fact that automated tests are not easily implemented for GUI programs. If you want to add some test code, please create `tests/` directory in the root directory of the whole project and put the test code in it.

## Pull Request

Do a pull request to the `main` branch of [muziing/Py2exe-GUI](https://github.com/muziing/Py2exe-GUI), and I will review the code and give feedbacks as soon as possible.

-----

# 贡献指南

非常感谢你愿意为 Py2exe-GUI 项目提供贡献，请阅读以下内容，遵守一些基本规则，以便项目保持良好状态快速发展。

## 开始编码之前

如果你准备对代码进行超过数十行的修改或新增，我强烈建议你先提交一个 issue，谈谈你想实现的东西。在投入很多精力之前，我们应该先讨论一下是否要这样做，也可以确保我们不重复工作。

## 编写代码

### 准备开发环境

开发环境相较于使用环境较为复杂，确保已经安装 Python 3.11+ 和 [Poetry](https://python-poetry.org/docs/#installation)，然后通过 Poetry 创建和安装开发环境：

```shell
cd Py2exe-GUI
poetry init
poetry install
```

> 如果你在国内使用 PyPI 源速度较慢，可以考虑取消注释 `pyproject.toml` 文件中的 `[[tool.poetry.source]]`
> 小节，启用国内镜像站。但注意不要将修改后的 `poetry.lock` 文件提交到 git 中。

还需要通过 [pre-commit](https://pre-commit.com/) 安装 git 钩子：

```shell
pre-commit install
```

### 代码风格

- 总体来讲，新增和修改的代码应接近原有代码的风格。尽量使代码有良好的可读性。
- 请使用 [Black](https://black.readthedocs.io/en/stable/) 格式化代码，确保所有代码风格与项目一致。开发环境中已经安装了 Black，配置使用方法可以参考[这篇文章](https://muzing.top/posts/a29e4743/)。
- 请为代码添加充分的[类型注解](https://muzing.top/posts/84a8da1c/)，并能通过 [mypy](https://mypy.readthedocs.io/en/stable/) 检查不报错。
- 请为模块、类、函数/方法、属性等添加 docstring 或注释，确保含义清晰易读。

### 文档

如果你实现了一些新功能，应考虑在 `docs/` 目录下添加相应的文档，或适当修改 `README.md` 来加以阐述。

### 测试

由于我的编程水平有限、GUI 程序不易实现自动化测试等原因，Py2exe-GUI 项目暂无测试。如果你想添加一些测试代码，请在整个项目的根目录下创建 `tests/` 目录，并将测试代码置于其中。

## 拉取请求

新建一个指向 [muziing/Py2exe-GUI](https://github.com/muziing/Py2exe-GUI) 的 `main` 分支的拉取请求，我将尽快 review`muziing/Py2exe-GUI` 的 `main` 分支的拉取请求，我将尽快 review 代码并给出反馈。
