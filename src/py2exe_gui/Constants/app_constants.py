# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

from .runtime_info import RUNTIME_INFO

APP_URLs = {
    "HOME_PAGE": "https://github.com/muziing/Py2exe-GUI",
    "BugTracker": "https://github.com/muziing/Py2exe-GUI/issues",
    "Pyinstaller_doc": "https://pyinstaller.org/",
}

if RUNTIME_INFO.language_code == "zh_CN":
    APP_URLs["Pyinstaller_doc"] = "https://muzing.gitbook.io/pyinstaller-docs-zh-cn/"


class AppConstant:
    """
    应用程序级的常量
    """

    NAME = "Py2exe-GUI"
    VERSION = "0.2.1"
    AUTHORS = ["muzing <muzi2001@foxmail.com>"]
    LICENSE = "GPL-3.0-or-later"
    HOME_PAGE = APP_URLs["HOME_PAGE"]
