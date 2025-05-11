"""Filesystem-related utilities."""

import re
from collections.abc import Callable
from enum import Enum, auto
from pathlib import Path

from bubop.exceptions import NoSuchFileOrDirectoryError


class FileType(Enum):
    """
    Enum to represent an entity on a filesystem and abstract operations on them.

    >>> ft = FileType.FILE
    >>> ft.exists(Path("/etc/passwd"))
    True
    >>> ft.exists(Path("/etc/"))
    False

    >>> ft = FileType.DIR
    >>> ft.exists(Path("/etc/passwd"))
    False
    >>> ft.exists(Path("/etc/"))
    True
    """

    FILE = auto()
    DIR = auto()
    FILE_OR_DIR = auto()

    def exists(self, path: Path) -> bool:
        """
        True if the give npath exists. Uses the appropriate function for the Filepath at hand.
        """
        return _file_type_to_exists_fn[self](path)


_file_type_to_exists_fn: dict[FileType, Callable[[Path], bool]] = {
    FileType.FILE: lambda p: p.is_file(),
    FileType.DIR: lambda p: p.is_dir(),
    FileType.FILE_OR_DIR: lambda p: p.exists(),
}

_file_type_to_not_exists_exc: dict[FileType, type[BaseException]] = {
    FileType.FILE: FileNotFoundError,
    FileType.DIR: NotADirectoryError,
    FileType.FILE_OR_DIR: NoSuchFileOrDirectoryError,
}


def valid_path(s: str, filetype=FileType.FILE_OR_DIR) -> Path:
    """Return a pathlib.Path from the given string.

    If the input does not correspond to a valid path, then raise an exception

    >>> valid_path("/etc")
    PosixPath...
    >>> valid_path("/etc/some-invalid-path")
    Traceback (most recent call last):
    bubop.exceptions.NoSuchFileOrDirectoryError: No such ...

    >>> valid_path("/etc", filetype=FileType.FILE)
    Traceback (most recent call last):
    FileNotFoundError: ...

    >>> valid_path("/etc/passwd", filetype=FileType.FILE)
    PosixPath...

    >>> valid_path("/etc/passwd", filetype=FileType.DIR)
    Traceback (most recent call last):
    NotADirectoryError: ...
    >>> valid_path("/etc", filetype=FileType.DIR)
    PosixPath...
    """
    path = Path(s).expanduser()
    if not filetype.exists(path):
        raise _file_type_to_not_exists_exc[filetype](path)

    return path


def valid_dir(s: str) -> Path:
    """Return a pathlib.Path from the given string.

    If the input does not correspond to a valid directory, then raise an exception

    >>> valid_dir("/etc/")
    PosixPath...
    >>> valid_dir("/etc/passwd")
    Traceback (most recent call last):
    NotADirectoryError: ...
    """
    return valid_path(s, filetype=FileType.DIR)


def valid_file(s: str) -> Path:
    """Return a pathlib.Path from the given string.

    If the input does not correspond to a valid directory, then raise an exception
    >>> valid_file("/etc/")
    Traceback (most recent call last):
    FileNotFoundError: ...
    >>> valid_file("/etc/passwd")
    PosixPath...
    """
    return valid_path(s, filetype=FileType.FILE)


def get_valid_filename(s: str) -> str:
    """Return a filename-compatible version of the given string s.

    :param s: String to be used as the base of the filename. You may also pass
              non-string objects that will however be able to convert to strings via the
              str operator.

    >>> get_valid_filename(r"5678^()^")
    '5678____'
    >>> get_valid_filename(r"a|string\\go/es||here")
    'a_string_go_es__here'
    >>> get_valid_filename(r"strin***g")
    'strin___g'

    .. seealso::

        `Stack Overflow thread <https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename>`_
    """
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "_", s)


def get_file_unique_id(p: Path) -> str:
    """Get a unique identifier for the filesystem entity at hand.

    Use a combination of device ID and inode.
    """

    stat = p.stat()
    return f"0x{stat.st_dev:02x}/0x{stat.st_ino:02x}"
