# -*- coding: utf-8 -*-

"""These rules checks ``import``s to be defined correctly."""

from wemake_python_styleguide.errors.base import BaseStyleViolation


class LocalFolderImportViolation(BaseStyleViolation):
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

    _error_tmpl = '{0} Found local folder import "{1}"'
    _code = 'Z100'


class NestedImportViolation(BaseStyleViolation):
    """
    This rule forbids to have nested imports in functions.

    Nested imports show that there's an issue with you design.
    So, you don't need nested imports, you need to refactor your code.

    Example::

        # Wrong:
        def some():
            from my_module import some_function

    Note:
        Returns Z101 as error code

    """

    _error_tmpl = '{0} Found nested import "{1}"'
    _code = 'Z101'


class FutureImportViolation(BaseStyleViolation):
    """
    This rule forbids to use ``__future__`` imports.

    Almost all ``__future__`` imports are legacy ``python2`` compatibility
    tools that are no longer required.

    Except, there are some new ones for ``python4`` support.

    Example::

        # Correct:
        from __future__ import annotations

        # Wrong:
        from __future__ import print_function

    Note:
        Returns Z102 as error code

    """

    _error_tmpl = '{0} Found future import "{1}"'
    _code = 'Z102'


class DottedRawImportViolation(BaseStyleViolation):
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

    _error_tmpl = '{0} Found dotted raw import "{1}"'
    _code = 'Z103'


class SameAliasImportViolation(BaseStyleViolation):
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

    _error_tmpl = '{0} Found same alias import "{1}"'
    _code = 'Z104'
