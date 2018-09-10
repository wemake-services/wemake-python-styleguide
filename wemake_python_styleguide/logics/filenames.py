# -*- coding: utf-8 -*-

from pathlib import PurePath
from typing import Iterable

from wemake_python_styleguide.options.defaults import MIN_MODULE_NAME_LENGTH


def _get_stem(file_path: str) -> str:
    return PurePath(file_path).stem


def is_stem_in_list(file_path: str, to_check: Iterable[str]) -> bool:
    """
    Checks either module's name is included in a search list.

    >>> is_stem_in_list('/some/module.py', ['other'])
    False

    >>> is_stem_in_list('partial/module.py', ['module'])
    True

    >>> is_stem_in_list('module.py', ['module'])
    True

    >>> is_stem_in_list('C:/User/package/__init__.py', ['__init__'])
    True

    """
    return _get_stem(file_path) in to_check


def is_magic(file_path: str) -> bool:
    """
    Checks either the given `file_path` contains the magic module name.

    >>> is_magic('__init__.py')
    True

    >>> is_magic('some.py')
    False

    >>> is_magic('/home/user/cli.py')
    False

    >>> is_magic('/home/user/__version__.py')
    True

    >>> is_magic('D:/python/__main__.py')
    True

    """
    stem = _get_stem(file_path)
    return stem.startswith('__') and stem.endswith('__')


def is_too_short_stem(
    file_path: str,
    min_length: int = MIN_MODULE_NAME_LENGTH,
) -> bool:
    """
    Checks either the file's stem fits into the minimum length.

    >>> is_too_short_stem('a.py')
    True

    >>> is_too_short_stem('prefix/b.py')
    True

    >>> is_too_short_stem('regular.py')
    False

    >>> is_too_short_stem('c:/package/abc.py', min_length=4)
    True

    """
    stem = _get_stem(file_path)
    return len(stem) < min_length
