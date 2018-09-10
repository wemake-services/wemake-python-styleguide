# -*- coding: utf-8 -*-

"""
These rules checks ``import``s to be defined correctly.

Explicit is better than implicit.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class LocalFolderImportViolation(ASTStyleViolation):
    """
    This rule forbids to have imports relative to the current folder.

    Example::

        # Correct:
        from my_package.version import get_version

        # Wrong:
        from .version import get_version
        from ..drivers import MySQLDriver

    Note:
        Returns Z100 as error code

    """

    error_template = '{0} Found local folder import "{1}"'
    code = 'Z100'


class NestedImportViolation(ASTStyleViolation):
    """
    This rule forbids to have nested imports in functions.

    Nested imports show that there's an issue with you design.
    So, you don't need nested imports, you need to refactor your code.

    Example::

        # Correct:
        from my_module import some_function

        def some(): ...

        # Wrong:
        def some():
            from my_module import some_function

    Note:
        Returns Z101 as error code

    """

    error_template = '{0} Found nested import "{1}"'
    code = 'Z101'


class FutureImportViolation(ASTStyleViolation):
    """
    This rule forbids to use ``__future__`` imports.

    Almost all ``__future__`` imports are legacy ``python2`` compatibility
    tools that are no longer required.

    Except, there are some new ones for ``python4`` support.
    See ``FUTURE_IMPORTS_WHITELIST`` for the full
    list of allowed future imports.

    Example::

        # Correct:
        from __future__ import annotations

        # Wrong:
        from __future__ import print_function

    Note:
        Returns Z102 as error code

    """

    error_template = '{0} Found future import "{1}"'
    code = 'Z102'


class DottedRawImportViolation(ASTStyleViolation):
    """
    This rule forbids to use imports like ``import os.path``.

    Example::

        # Correct:
        from os import path

        # Wrong:
        import os.path

    Note:
        Returns Z103 as error code

    """

    error_template = '{0} Found dotted raw import "{1}"'
    code = 'Z103'


class SameAliasImportViolation(ASTStyleViolation):
    """
    This rule forbids to use the same alias as the original name in imports.

    Example::

        # Correct:
        from os import path

        # Wrong:
        from os import path as path

    Note:
        Returns Z104 as error code

    """

    error_template = '{0} Found same alias import "{1}"'
    code = 'Z104'
