# -*- coding: utf-8 -*-

from pathlib import PurePath


def get_stem(file_path: str) -> str:
    """
    Returns the last element of path without extension.

    >>> get_stem('/some/module.py')
    'module'

    >>> get_stem('C:/User/package/__init__.py')
    '__init__'

    >>> get_stem('c:/package/abc.py')
    'abc'

    >>> get_stem('episode2.py')
    'episode2'

    """
    return PurePath(file_path).stem
