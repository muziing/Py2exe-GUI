# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

import locale
import os
import pathlib
import warnings
from typing import Optional, Union

from PySide6.QtCore import QByteArray, QFile, QFileInfo, QIODevice


class QtFileOpen:
    """
    通过 QFile 读写文件的上下文管理器 \n
    使与 Python 的 "with open() as" 语句风格统一 \n

    使用举例：

    with QtFileOpen("./test.txt", "rt", encoding="utf-8") as f:
        print(f.read())
    """

    def __init__(
        self,
        file: Union[str, bytes, os.PathLike[str]],
        mode="r",
        encoding: Optional[str] = None,
    ):
        """
        :param file: 文件路径
        :param mode: 打开模式（暂时只支持文本读取）
        :param encoding: 文本文件编码，留空则自动处理
        """

        # 预处理文件路径，防止在 Windows 平台下 QFile 只能处理 '/' 导致的问题
        file_path = self.deal_path(file)

        # 分析模式是否合法、返回正确的 FileIo 类实例
        # https://docs.python.org/zh-cn/3/library/functions.html#open
        if "b" not in mode:
            # 文本模式
            self.io_obj = PyQTextFileIo(file_path, mode, encoding)
        else:
            # 二进制模式（暂不支持）
            # self.io_obj = PyQByteFileIo(file, mode)
            raise ValueError("暂不支持该模式")

    def __enter__(self):
        return self.io_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.io_obj.close()

    @staticmethod
    def deal_path(path: Union[str, bytes, os.PathLike[str]]) -> str:
        """
        预处理文件路径，统一成字符串类型、确保使用 posix / 风格
        :param path: 文件路径
        :return: 使用正斜杠（/）的路径字符串
        """

        # 若路径以字节串传入，则先处理成字符串
        if isinstance(path, bytes):
            path = path.decode("utf-8")

        return str(pathlib.PurePath(path).as_posix())


class PyQTextFileIo:
    """
    将 QFile 中处理文本文件读写的部分封装成 Python的 io 风格
    目前只支持读取，不支持写入
    """

    def __init__(self, file: str, mode, encoding: Optional[str] = None):
        """
        :param file: 文件路径
        :param mode: 打开模式
        :param encoding: 文本编码
        """

        self._detect_error(file)
        self._file = QFile(file)

        if encoding is not None:
            self.encoding = encoding
        else:
            # 用户未指定编码，则使用当前平台默认编码
            self.encoding = locale.getencoding()

        self.mode = self._parse_mode(mode)
        self._file.open(self.mode)

    @staticmethod
    def _detect_error(input_file: str) -> None:
        """
        检查传入的文件是否存在错误，如有则抛出对应的异常 \n
        :param input_file: 文件路径
        """

        file_info = QFileInfo(input_file)
        if file_info.isDir():
            raise IsADirectoryError(f"File '{input_file}' is a directory.")
        if not file_info.exists():
            raise FileNotFoundError(f'File "{input_file}" not found.')

    @staticmethod
    def _parse_mode(py_mode: str) -> QIODevice.OpenModeFlag:
        """
        解析文件打开模式，将 Python open() 风格转换至 QIODevice.OpenModeFlag
        https://docs.python.org/zh-cn/3/library/functions.html#open
        https://doc.qt.io/qt-6/qiodevicebase.html#OpenModeFlag-enum
        :return: QIODevice.OpenModeFlag
        """

        qt_mode: QIODevice.OpenModeFlag = QIODevice.OpenModeFlag.Text

        # 暂不支持写入
        if "r" in py_mode and "+" not in py_mode:
            qt_mode = qt_mode | QIODevice.OpenModeFlag.ReadOnly
        elif "w" in py_mode:
            qt_mode = qt_mode | QIODevice.OpenModeFlag.WriteOnly
        elif "+" in py_mode:
            qt_mode = qt_mode | QIODevice.OpenModeFlag.ReadWrite

        if "x" in py_mode:
            qt_mode = qt_mode | QIODevice.OpenModeFlag.NewOnly

        return qt_mode

    @staticmethod
    def qba_to_str(qba: QByteArray, encoding: str = locale.getencoding()) -> str:
        """
        将 QByteArray 转换为 str
        """

        return qba.data().decode(encoding=encoding)

    def readable(self) -> bool:
        """
        当前文件是否可读 \n
        :return: isReadable
        """

        return self._file.isReadable()

    def read(self, size: int = -1) -> str:
        """
        模仿 `io.TextIOBase.read` 的行为，读取流中的文本。 \n
        从流中读取至多 size 个字符并以单个 str 的形式返回。 如果 size 为负值或 None，则读取至 EOF。 \n
        https://docs.python.org/3/library/io.html#io.TextIOBase.read
        :param size: 读取的字符数，负值或 None 表示一直读取直到 EOF
        :return: 文件中读出的文本内容
        """

        if not self.readable():
            raise PermissionError(f"File '{self._file.fileName()}' is not Readable.")

        if size < 0 or size is None:
            # 读取文件，并将 QByteArray 转为 str
            text = self.qba_to_str(self._file.readAll(), encoding=self.encoding)
        else:
            # 已知问题：性能太差
            # PySide6.QtCore.QIODevice.read(maxlen) 以字节而非字符方式计算长度，行为不一致
            # 而 QTextStream 对字符编码支持太差，许多编码并不支持
            text_all = self.qba_to_str(self._file.readAll(), self.encoding)
            text = text_all[0:size]  # 性能太差

        return text

    def readline(self, size: int = -1, /) -> str:
        """
        模仿 `io.TextIOBase.readline` 的行为，读取文件中的一行。 \n
        https://docs.python.org/3/library/io.html#io.TextIOBase.readline
        :param size: 如果指定了 size ，最多将读取 size 个字符。
        :return: 单行文本
        """

        if not self.readable():
            raise PermissionError(f"File '{self._file.fileName()}' is not Readable.")

        if self._file.atEnd():
            warnings.warn(
                f"Trying to read a line at the end of the file '{self._file.fileName()}'.",
                Warning,
                stacklevel=1,
            )
            return ""
        else:
            if size == 0:
                return ""
            else:
                line = self.qba_to_str(self._file.readLine(), self.encoding)
                if size < 0:
                    return line
                else:
                    return line[0:size]

    def readlines(self, hint: int = -1, /) -> list[str]:
        """
        模仿 `io.IOBase.readlines()` 的行为，返回由所有行组成的字符串列表。 \n
        Known issue： slower than `readline()` \n
        https://docs.python.org/3/library/io.html#io.IOBase.readlines
        :param hint: 要读取的字符数
        :return: 文本内容所有行组成的列表
        """

        if not self.readable():
            raise PermissionError(f"File '{self._file.fileName()}' is not Readable.")

        if hint <= 0 or hint is None:
            temp = self.qba_to_str(self._file.readAll(), self.encoding)
            all_lines = temp.splitlines(keepends=True)
        else:
            all_lines = []
            char_num = 0
            while char_num <= hint and not self._file.atEnd():
                new_line = self.readline()
                all_lines.append(new_line)
                char_num += len(new_line)

        return all_lines

    def close(self) -> None:
        """
        关闭打开的文件对象 \n
        """

        self._file.close()
