# -*- coding: utf-8 -*-

"""
Naming is hard! It is in fact one of the two hardest problems.

These checks are required to make your application easier to read
and understand by multiple people over the long period of time.

Naming convention
-----------------

Our naming convention tries to cover all possible cases.
It is partially automated with this linter, but:

- Some rules are still WIP
- Some rules will never be automated, code reviews to the rescue!

General
~~~~~~~

- Use only ``ASCII`` chars for names
- Do not use transliteration from any other languages, translate names instead
- Use clear names, do not use words that do not mean anything like ``obj``
- Use names of an appropriate length: not too short, not too long
- Protected members should use underscore as the first char
- Private names with two leading underscores are not allowed
- If you need to explicitly state that variable is unused,
  prefix it with ``_`` or just use ``_`` as a name
- Do not use variables that are stated to be unused, rename them when using
- Do not use consecutive underscores
- When writing abbreviations in ``UpperCase``
  capitalize all letters: ``HTTPAddress``
- When writing abbreviations in ``snake_case`` use lowercase: ``http_address``
- When writing numbers in ``snake_case``
  do not use extra ``_`` before numbers as in ``http2_protocol``

Packages
~~~~~~~~

- Packages must use ``snake_case``
- One word for a package is the most preferable name

Modules
~~~~~~~

- Modules must use ``snake_case``
- Module names must not overuse magic names
- Module names must be valid Python identifiers

Classes
~~~~~~~

- Classes must use ``UpperCase``
- Python's built-in classes, however are typically lowercase words
- Exception classes must end with ``Error``

Instance attributes
~~~~~~~~~~~~~~~~~~~

- Instance attributes must use ``snake_case`` with no exceptions

Class attributes
~~~~~~~~~~~~~~~~

- Class attributes must use ``snake_case``  with no exceptions

Functions and methods
~~~~~~~~~~~~~~~~~~~~~

- Functions and methods must use ``snake_case`` with no exceptions

Method and function arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Instance methods must have their first argument named ``self``
- Class methods must have their first argument named ``cls``
- Metaclass methods must have their first argument named ``mcs``
- Python's ``*args`` and ``**kwargs`` should be default names
  when just passing these values to some other method/function,
  unless you want to use these values in place, then name them explicitly
- Keyword-only arguments must be separated from other arguments with ``*``

Global (module level) variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Global variables must use ``CONSTANT_CASE``
- Unless other is required by the API, example: ``urlpatterns`` in Django

Variables
~~~~~~~~~

- Variables must use ``snake_case`` with no exceptions
- When variable is unused it must be prefixed with an underscore: ``_user``

Type aliases
~~~~~~~~~~~~

- Must use ``UpperCase`` as real classes
- Must not contain word ``type`` in its name
- Generic types should be called ``TT`` or ``KT`` or ``VT``
- Covariant and contravariant types
  should be marked with ``Cov`` and ``Contra`` suffixes,
  in this case one letter can be dropped: ``TCov`` and ``KContra``

.. currentmodule:: wemake_python_styleguide.violations.naming

Summary
-------

.. autosummary::
   :nosignatures:

   WrongModuleNameViolation
   WrongModuleMagicNameViolation
   WrongModuleNamePatternViolation
   WrongVariableNameViolation
   TooShortNameViolation
   PrivateNameViolation
   SameAliasImportViolation
   UnderscoredNumberNameViolation
   UpperCaseAttributeViolation
   ConsecutiveUnderscoresInNameViolation
   ReservedArgumentNameViolation
   TooLongNameViolation
   UnicodeNameViolation

Module names
------------

.. autoclass:: WrongModuleNameViolation
.. autoclass:: WrongModuleMagicNameViolation
.. autoclass:: WrongModuleNamePatternViolation

General names
-------------

.. autoclass:: WrongVariableNameViolation
.. autoclass:: TooShortNameViolation
.. autoclass:: PrivateNameViolation
.. autoclass:: SameAliasImportViolation
.. autoclass:: UnderscoredNumberNameViolation
.. autoclass:: UpperCaseAttributeViolation
.. autoclass:: ConsecutiveUnderscoresInNameViolation
.. autoclass:: ReservedArgumentNameViolation
.. autoclass:: TooLongNameViolation
.. autoclass:: UnicodeNameViolation

"""

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    MaybeASTViolation,
    SimpleViolation,
)


@final
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

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong module name'
    code = 100


@final
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

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong module magic name'
    code = 101


@final
class WrongModuleNamePatternViolation(SimpleViolation):
    """
    Forbids to use module names that do not match our pattern.

    Reasoning:
        Module names must be valid python identifiers.
        And just like the variable names - module names should be consistent.
        Ideally, they should follow the same rules.
        For ``python`` world it is common to use ``snake_case`` notation.

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

    .. versionadded:: 0.1.0

    """

    error_template = 'Found incorrect module name pattern'
    code = 102


# General names:

@final
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

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong variable name: {0}'
    code = 110


@final
class TooShortNameViolation(MaybeASTViolation):
    """
    Forbids to have too short variable or module names.

    Reasoning:
        It is hard to understand what the variable means and why it is used,
        if it's name is too short.

    Solution:
        Think of another name. Give more context to it.

    This rule checks: modules, variables, attributes,
    functions, methods, and classes.

    Example::

        # Correct:
        x_coordinate = 1
        abscissa = 2

        # Wrong:
        x = 1
        y = 2

    Configuration:
        This rule is configurable with ``--min-name-length``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MIN_NAME_LENGTH`

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.4.0

    """

    error_template = 'Found too short name: {0}'
    code = 111


@final
class PrivateNameViolation(MaybeASTViolation):
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

    This rule checks: modules, variables, attributes, functions, and methods.

    Example::

        # Correct:
        def _collect_coverage(self): ...

        # Wrong:
        def __collect_coverage(self): ...

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.4.0

    """

    error_template = 'Found private name pattern: {0}'
    code = 112


@final
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

    .. versionadded:: 0.1.0

    """

    error_template = 'Found same alias import: {0}'
    code = 113


@final
class UnderscoredNumberNameViolation(MaybeASTViolation):
    """
    Forbids to have names with underscored numbers pattern.

    Reasoning:
        This is done for consistency in naming.

    Solution:
        Do not put an underscore between text and numbers, that is confusing.
        Rename your variable or modules to not include underscored numbers.

    This rule checks: modules, variables, attributes,
    functions, method, and classes.
    Please, note that putting an underscore that replaces ``-`` in some
    names between numbers is fine, example: ``ISO-123-456`` would became
    ``iso123_456``.

    Example::

        # Correct:
        star_wars_episode2 = 'awesome!'
        iso123_456 = 'some data'

        # Wrong:
        star_wars_episode_2 = 'not so awesome'
        iso_123_456 = 'some data'

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.4.0

    """

    error_template = 'Found underscored name pattern: {0}'
    code = 114


@final
class UpperCaseAttributeViolation(ASTViolation):
    """
    Forbids to use anything but ``snake_case`` for naming class attributes.

    Reasoning:
        Constants with upper-case names belong on a module level.

    Solution:
        Move your constants to the module level.
        Rename your variables so that they conform
        to ``snake_case`` convention.

    Example::

        # Correct:
        MY_MODULE_CONSTANT = 1
        class A(object):
            my_attribute = 42

        # Wrong:
        class A(object):
            MY_CONSTANT = 42

    .. versionadded:: 0.3.0

    """

    error_template = 'Found upper-case constant in a class: {0}'
    code = 115


@final
class ConsecutiveUnderscoresInNameViolation(MaybeASTViolation):
    """
    Forbids to use more than one consecutive underscore in variable names.

    Reasoning:
        This is done to gain extra readability.
        This naming rule already exist for module names.

    Example::

        # Correct:
        some_value = 5
        __magic__ = 5

        # Wrong:
        some__value = 5

    This rule checks: modules, variables, attributes, functions, and methods.

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.4.0

    """

    error_template = 'Found consecutive underscores name: {0}'
    code = 116


@final
class ReservedArgumentNameViolation(ASTViolation):
    """
    Forbids to name your variables as ``self``, ``cls``, and ``mcs``.

    Reasoning:
        These names are special, they should only be used as first
        arguments inside methods.

    Example::

        # Correct:
        class Test(object):
            def __init__(self):
                ...

        # Wrong:
        cls = 5
        lambda self: self + 12

    This rule checks: functions and methods.
    Having any reserved names in ``lambda`` functions is not allowed.

    .. versionadded:: 0.5.0

    """

    error_template = 'Found name reserved for first argument: {0}'
    code = 117


@final
class TooLongNameViolation(MaybeASTViolation):
    """
    Forbids to have long short variable or module names.

    Reasoning:
        Too long names are unreadable.
        It is better to use shorter alternative.
        Long names also indicate that this variable is too complex,
        maybe it may require some documentation.

    Solution:
        Think of another name. Give less context to it.

    This rule checks: modules, variables, attributes,
    functions, methods, and classes.

    Example::

        # Correct:
        total_price = 25
        average_age = 45

        # Wrong:
        final_price_after_fifteen_percent_sales_tax_and_gratuity = 30
        total_age_of_all_participants_in_the_survey_divided_by_twelve = 2

    Configuration:
        This rule is configurable with ``--max-name-length``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_NAME_LENGTH`

    .. versionadded:: 0.5.0

    """

    error_template = 'Found too long name: {0}'
    code = 118


@final
class UnicodeNameViolation(MaybeASTViolation):
    """
    Restrict unicode names.

    Reasoning:
        This should be forbidden for sanity, readability, and writability.

    Solution:
        Rename your entities so that they contain only ASCII symbols.

    This rule checks: modules, variables, attributes,
    functions, methods, and classes.

    Example::

        # Correct:
        some_variable = 'Text with russian: русский язык'

        # Wrong:
        переменная = 42
        some_變量 = ''

    .. versionadded:: 0.5.0

    """

    error_template = 'Found unicode name: {0}'
    code = 119
