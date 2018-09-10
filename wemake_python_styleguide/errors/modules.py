# -*- coding: utf-8 -*-

"""
These rules checks that modules are defined correctly.

Please, take a note that these rules are not applied to packages.
"""

from wemake_python_styleguide.errors.base import SimpleStyleViolation


class WrongModuleNameViolation(SimpleStyleViolation):
    """
    This rule forbids to use blacklisted module names.

    See ``BAD_MODULE_NAMES`` for the full list of bad module names.

    Example::

        # Correct:
        github.py
        views.py

        # Wrong:
        utils.py
        helpers.py

    Note:
        Returns Z400 as error code

    """

    should_use_text = False
    error_template = '{0} Found wrong module name'
    code = 'Z400'


class WrongModuleMagicNameViolation(SimpleStyleViolation):
    """
    This rule forbids to use any magic names except whitelisted ones.

    See ``MAGIC_MODULE_NAMES_WHITELIST`` for the full list of allowed
    magic module names.

    Example::

        # Correct:
        __init__.py
        __main__.py

        # Wrong:
        __version__.py

    Note:
        Returns Z401 as error code

    """

    should_use_text = False
    error_template = '{0} Found wrong module magic name'
    code = 'Z401'


class TooShortModuleNameViolation(SimpleStyleViolation):
    """
    This rule forbids to use module name shorter than some breakpoint.

    Too short module names are not expressive enough.
    We will have to open the source code to find out what is going on there.

    This rule is configurable with ``--min-module-name-length``.

    Note:
        Returns Z402 as error code

    """

    should_use_text = False
    error_template = '{0} Found too short module name'
    code = 'Z402'
