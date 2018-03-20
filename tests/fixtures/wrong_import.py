# -*- coding: utf-8 -*-

"""
This file contains all imports that are prohibited.
"""

from . import package
from .module import some_function

from .. import some
from ..other import other_function

wrong = __import__('this')


def check_import_inside_function():
    import ast
    return ast


def check_import_from_inside_function():
    from os import path
    return path


# This line is required to use imports:
print(package, some_function, some, other_function)
