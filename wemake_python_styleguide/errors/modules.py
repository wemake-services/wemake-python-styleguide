# -*- coding: utf-8 -*-

"""
These rules checks that modules are defined correctly.

Please, take a note that these rules are not applied to packages.

Things we check here:

1. Naming
2. Contents: some modules must have contents, some must not

"""

from wemake_python_styleguide.errors.base import SimpleStyleViolation


class WrongModuleNameViolation(SimpleStyleViolation):
    """
    Forbids to use blacklisted module names.

    Reasoning:
        Some module names are not expressive enough.
        It is hard to tell what you can find inside the ``utils.py`` module.

    Solution:
        Rename your module, reorganize the contents.

    See
    :py:data:`~wemake_python_styleguide.constants.BAD_MODULE_NAMES`
    for the full list of bad module names.

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
    code = 400


class WrongModuleMagicNameViolation(SimpleStyleViolation):
    """
    Forbids to use any magic names except whitelisted ones.

    Reasoning:
        Do not fall in love with magic. There's no good reason to use
        magic names, when you can use regular names.

    See
    :py:data:`~wemake_python_styleguide.constants.MAGIC_MODULE_NAMES_WHITELIST`
    for the full list of allowed magic module names.

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
    code = 401


class TooShortModuleNameViolation(SimpleStyleViolation):
    """
    Forbids to use module name shorter than some breakpoint.

    Reasoning:
        Too short module names are not expressive enough.
        We will have to open the code to find out what is going on there.

    Solution:
        Rename the module.

    This rule is configurable with ``--min-module-name-length``.

    Note:
        Returns Z402 as error code

    """

    should_use_text = False
    error_template = '{0} Found too short module name'
    code = 402


class WrongModuleNameUnderscoresViolation(SimpleStyleViolation):
    """
    Forbids to use multiple underscores in a row in a module name.

    Reasoning:
        It is hard to tell how many underscores are there: two or three?

    Solution:
        Keep just one underscore in a module name.

    Example::
        # Correct:
        __init__.py
        some_module_name.py
        test.py

        # Wrong:
        some__wrong__name.py
        my__module.py
        __fake__magic__.py

    Note:
        Returns Z403 as error code

    """

    should_use_text = False
    error_template = '{0} Found repeating underscores in a module name'
    code = 403


class WrongModuleNamePatternViolation(SimpleStyleViolation):
    """
    Forbids to use module names that do not match our pattern.

    Reasoning:
        Just like the variable names - module names should be consistent.
        Ideally, they should follow the same rules.
        For ``python`` world it is common to use `snake_case` notation.

    We use
    :py:data:`~wemake_python_styleguide.constants.MODULE_NAME_PATTERN`
    to validate the module names.

    Example::
        # Correct:
        __init__.py
        some_module_name.py
        test12.py

        # Wrong:
        _some.py
        MyModule.py
        0001_migration.py

    Note:
        Returns Z404 as error code

    """

    should_use_text = False
    error_template = '{0} Found incorrect module name pattern'
    code = 404
