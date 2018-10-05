# -*- coding: utf-8 -*-

"""
Naming is hard! It is in fact one of the two hardest problems.

These checks are required to make your application easier to read
and understand by multiple people over the long period of time.

Note:

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Readability counts.
    Namespaces are one honking great idea -- let's do more of those!


Naming convention
-----------------

Our naming convention tries to cover all possible cases.
It is partially automated with this linter, but

- Some rules are still WIP
- Some rules will never be automated, code reviews to the rescue!

General
~~~~~~~

- Use clear names, do not use words that do not mean anything like ``obj``
- Use names of an appropriate length: not too short, not too long
- Protected members should use underscore as the first char
- Private names are not allowed
- When writing abbreviations in ``UpperCase``
  capitalize all letters: ``HTTPAddress``
- When writting abbreviations in ``snake_case`` use lowercase: ``http_address``
- When writting numbers in ``snake_case``
  do not use extra ``_`` as in ``http2_protocol``

Packages
~~~~~~~~

- Packages should use ``snake_case``
- One word for a package is the most prefitable name

Modules
~~~~~~~

- Modules should use ``snake_case``
- Module names should not be too short
- Module names should not overuse magic names
- Module names should be valid Python variable names

Classes
~~~~~~~

- Classes should use ``UpperCase``
- Python's built-in classes, however are typically lowercase words
- Exception classes should end with ``Error``

Instance attributes
~~~~~~~~~~~~~~~~~~~

- Instance attributes should use ``snake_case`` with no exceptions

Class attributes
~~~~~~~~~~~~~~~~

- Class attributes should use ``snake_case``  with no exceptions

Functions and methods
~~~~~~~~~~~~~~~~~~~~~

- Functions and methods should use ``snake_case`` with no exceptions

Method arguments
~~~~~~~~~~~~~~~~

- Instance methods should have their first argument named ``self``
- Class methods should have their first argument named ``cls``
- Metaclass methods should have their first argument named ``mcs``
- When argument is unused it should be prefixed with an underscore
- Python's ``*args`` and ``**kwargs`` should be default names
  when just passing these values to some other method/function
- Unless you want to use these values in place, then name them explicitly
- Keyword-only arguments might be separated from other arguments with ``*``

Global (module level) variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Global variables should use ``CONSTANT_CASE``
- Unless other is required by the API, example: ``urlpatterns`` in Django

Variables
~~~~~~~~~

- Variables should use ``snake_case``
- When some variable is unused it should be prefixed with an underscore

Type aliases
~~~~~~~~~~~~

- Should use ``UpperCase`` as real classes
- Should not contain word ``type`` in its name
- Generic types should be called ``TT`` or ``KK`` or ``VV``
- Covariant and contravariant types
  should be marked with ``Cov`` and ``Contra`` suffixes
- In this case one letter can be dropped: ``TCov`` and ``KContra``

.. currentmodule:: wemake_python_styleguide.violations.naming

Summary
-------

.. autosummary::
   :nosignatures:

   WrongModuleNameViolation
   WrongModuleMagicNameViolation
   TooShortModuleNameViolation
   WrongModuleNameUnderscoresViolation
   WrongModuleNamePatternViolation
   WrongVariableNameViolation
   TooShortVariableNameViolation
   PrivateNameViolation
   SameAliasImportViolation

Module names
------------

.. autoclass:: WrongModuleNameViolation
.. autoclass:: WrongModuleMagicNameViolation
.. autoclass:: TooShortModuleNameViolation
.. autoclass:: WrongModuleNameUnderscoresViolation
.. autoclass:: WrongModuleNamePatternViolation

Variable names
--------------

.. autoclass:: WrongVariableNameViolation
.. autoclass:: TooShortVariableNameViolation
.. autoclass:: PrivateNameViolation
.. autoclass:: SameAliasImportViolation

"""

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    SimpleViolation,
)


class WrongModuleNameViolation(SimpleViolation):
    """
    Forbids to use blacklisted module names.

    Reasoning:
        Some module names are not expressive enough.
        It is hard to tell what you can find inside the ``utils.py`` module.

    Solution:
        Rename your module, reorganize the contents.

    See
    :py:data:`~wemake_python_styleguide.constants.MODULE_NAMES_BLACKLIST`
    for the full list of bad module names.

    Example::

        # Correct:
        github.py
        views.py

        # Wrong:
        utils.py
        helpers.py

    Note:
        Returns Z100 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found wrong module name'
    code = 100


class WrongModuleMagicNameViolation(SimpleViolation):
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
        Returns Z101 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found wrong module magic name'
    code = 101


class TooShortModuleNameViolation(SimpleViolation):
    """
    Forbids to use module name shorter than some breakpoint.

    Reasoning:
        Too short module names are not expressive enough.
        We will have to open the code to find out what is going on there.

    Solution:
        Rename the module.

    This rule is configurable with ``--min-module-name-length``.

    Note:
        Returns Z102 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found too short module name'
    code = 102


class WrongModuleNameUnderscoresViolation(SimpleViolation):
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
        Returns Z103 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found repeating underscores in a module name'
    code = 103


class WrongModuleNamePatternViolation(SimpleViolation):
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
        Returns Z104 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found incorrect module name pattern'
    code = 104


# Variables

class WrongVariableNameViolation(ASTViolation):
    """
    Forbids to have blacklisted variable names.

    Reasoning:
        We have found some names that are not expressive enough.
        However, they appear in the code more than often.
        All names that we forbid to use could be improved.

    Solution:
        Try to use more specific name instead.
        If you really want to use any of the names from the list,
        add a prefix or suffix to it. It will serve you well.

    See
    :py:data:`~wemake_python_styleguide.constants.VARIABLE_NAMES_BLACKLIST`
    for the full list of blacklisted variable names.

    Example::

        # Correct:
        html_node_item = None

        # Wrong:
        item = None

    Note:
        Returns Z110 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found wrong variable name "{0}"'
    code = 110


class TooShortVariableNameViolation(ASTViolation):
    """
    Forbids to have too short variable names.

    Reasoning:
        It is hard to understand what the variable means and why it is used,
        if it's name is too short.

    Solution:
        Think of another name. Give more context to it.

    This rule is configurable with ``--min-variable-length``.

    Example::

        # Correct:
        x_coordinate = 1
        abscissa = 2

        # Wrong:
        x = 1
        y = 2

    Note:
        Returns Z111 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found too short name "{0}"'
    code = 111


class PrivateNameViolation(ASTViolation):
    """
    Forbids to have private name pattern.

    Reasoning:
        Private is not private in ``python``.
        So, why should we pretend it is?
        This might lead to some serious design flaws.

    Solution:
        Rename your variable or method to be protected.
        Think about your design, why do you want to make it private?
        Are there any other ways to achieve what you want?

    This rule checks: variables, attributes, functions, and methods.

    Example::

        # Correct:
        def _collect_coverage(self): ...

        # Wrong:
        def __collect_coverage(self): ...

    Note:
        Returns Z112 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found private name pattern "{0}"'
    code = 112


class SameAliasImportViolation(ASTViolation):
    """
    Forbids to use the same alias as the original name in imports.

    Reasoning:
        Why would you even do this in the first place?

    Example::

        # Correct:
        from os import path

        # Wrong:
        from os import path as path

    Note:
        Returns Z113 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found same alias import "{0}"'
    code = 113
