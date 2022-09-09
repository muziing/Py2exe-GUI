import sys

"""
为使本软件成为跨平台工具，需要对三大平台的差异部分进行额外处理
"""

if sys.platform.startswith("win32"):
    print("Windows")
elif sys.platform.startswith("linux"):
    print("Linux")
elif sys.platform.startswith("darwin"):
    print("macOS")
