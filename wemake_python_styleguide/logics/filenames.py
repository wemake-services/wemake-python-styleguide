# -*- coding: utf-8 -*-

from pathlib import PurePath
from typing import Iterable
from typing.re import Pattern

from wemake_python_styleguide import constants
from wemake_python_styleguide.options import defaults


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
    min_length: int = defaults.MIN_MODULE_NAME_LENGTH,
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


def is_matching_pattern(
    file_path: str,
    pattern: Pattern = constants.MODULE_NAME_PATTERN,
) -> bool:
    r"""
    Checks either the file's stem matches the given pattern or not.

    >>> is_matching_pattern('some.py')
    True

    >>> is_matching_pattern('__init__.py')
    True

    >>> is_matching_pattern('MyModule.py')
    False

    >>> import re
    >>> is_matching_pattern('123.py', pattern=re.compile(r'\d{3}'))
    True

    """
    stem = _get_stem(file_path)
    return pattern.match(stem) is not None
