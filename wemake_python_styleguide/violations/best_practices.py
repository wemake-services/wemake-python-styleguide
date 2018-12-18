# -*- coding: utf-8 -*-

"""
These checks ensures that you follow the best practices.

The source for these best practices is hidden inside countless hours
we have spent debugging software or reviewing it.

How do we find an inspiration for new rules?
We find some ugly code during code reviews and audits.
Then we forbid to use it forever.
So, this error will never return to our codebase.

.. currentmodule:: wemake_python_styleguide.violations.best_practices

Summary
-------

.. autosummary::
   :nosignatures:

   WrongMagicCommentViolation
   WrongDocCommentViolation
   WrongModuleMetadataViolation
   EmptyModuleViolation
   InitModuleHasLogicViolation
   WrongKeywordViolation
   WrongFunctionCallViolation
   FutureImportViolation
   RaiseNotImplementedViolation
   BaseExceptionViolation
   BooleanPositionalArgumentViolation
   NestedFunctionViolation
   NestedClassViolation
   MagicNumberViolation
   StaticMethodViolation
   BadMagicMethodViolation
   NestedImportViolation
   RedundantLoopElseViolation
   RedundantFinallyViolation
   ReassigningVariableToItselfViolation
   YieldInsideInitViolation
   ProtectedModuleViolation
   ProtectedAttributeViolation
   LambdaInsideLoopViolation
   UnreachableCodeViolation
   StatementHasNoEffectViolation
   MultipleAssignmentsViolation
   IncorrectUnpackingViolation
   DuplicateExceptionViolation

Comments
--------

.. autoclass:: WrongMagicCommentViolation
.. autoclass:: WrongDocCommentViolation

Modules
-------

.. autoclass:: WrongModuleMetadataViolation
.. autoclass:: EmptyModuleViolation
.. autoclass:: InitModuleHasLogicViolation

Builtins
--------
.. autoclass:: WrongKeywordViolation
.. autoclass:: WrongFunctionCallViolation
.. autoclass:: FutureImportViolation
.. autoclass:: RaiseNotImplementedViolation
.. autoclass:: BaseExceptionViolation
.. autoclass:: BooleanPositionalArgumentViolation

Design
------

.. autoclass:: NestedFunctionViolation
.. autoclass:: NestedClassViolation
.. autoclass:: MagicNumberViolation
.. autoclass:: StaticMethodViolation
.. autoclass:: BadMagicMethodViolation
.. autoclass:: NestedImportViolation
.. autoclass:: RedundantLoopElseViolation
.. autoclass:: RedundantFinallyViolation
.. autoclass:: ReassigningVariableToItselfViolation
.. autoclass:: YieldInsideInitViolation
.. autoclass:: ProtectedModuleViolation
.. autoclass:: ProtectedAttributeViolation
.. autoclass:: LambdaInsideLoopViolation
.. autoclass:: UnreachableCodeViolation
.. autoclass:: StatementHasNoEffectViolation
.. autoclass:: MultipleAssignmentsViolation
.. autoclass:: IncorrectUnpackingViolation
.. autoclass:: DuplicateExceptionViolation

"""

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    SimpleViolation,
    TokenizeViolation,
)


@final
class WrongMagicCommentViolation(SimpleViolation):
    """
    Restricts to use several control (or magic) comments.

    We do not allow to use:

    1. ``# noqa`` comment without specified violations
    2. ``# type: some_type`` comments to specify a type for ``typed_ast``

    Reasoning:
        We cover several different use-cases in a single rule.
        ``# noqa`` comment is restricted because it can hide other violations.
        ``# type: some_type`` comment is restricted because
        we can already use type annotations instead.

    Solution:
        Use ``# noqa`` comments with specified error types.
        Use type annotations to specify types.

    We still allow to use ``# type: ignore`` comment.
    Since sometimes it is totally required.

    Example::

        # Correct:
        type = MyClass.get_type()  # noqa: A001
        coordinate: int = 10
        some.int_field = 'text'  # type: ignore

        # Wrong:
        type = MyClass.get_type()  # noqa
        coordinate = 10  # type: int

    .. versionadded:: 0.1.0

    """

    code = 400
    error_template = 'Found wrong magic comment: {0}'


@final
class WrongDocCommentViolation(TokenizeViolation):
    """
    Forbids to use empty doc comments (``#:``).

    Reasoning:
        Doc comments are used to provide a documentation.
        But supplying empty doc comments breaks this use-case.
        It is unclear why they can be used with no contents.

    Solution:
        Add some documentation to this comment. Or remove it.

    Empty doc comments are not caught by the default ``pycodestyle`` checks.

    Example::

        # Correct:
        #: List of allowed names:
        NAMES_WHITELIST = ['feature', 'bug', 'research']

        # Wrong:
        #:
        NAMES_WHITELIST = ['feature', 'bug', 'research']

    .. versionadded:: 0.1.0

    """

    code = 401
    error_template = 'Found wrong doc comment'


# Modules:

@final
class WrongModuleMetadataViolation(ASTViolation):
    """
    Forbids to have some module level variables.

    Reasoning:
        We discourage using module variables like ``__author__``,
        because code should not contain any metadata.

    Solution:
        Place all the metadata in ``setup.py``,
        ``setup.cfg``, or ``pyproject.toml``.
        Use proper docstrings and packaging classifiers.
        Use ``pkg_resources`` if you need to import this data into your app.

    See
    :py:data:`~wemake_python_styleguide.constants.MODULE_METADATA_VARIABLES_BLACKLIST`
    for full list of bad names.

    Example::

        # Wrong:
        __author__ = 'Nikita Sobolev'
        __version__ = 0.1.2

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong metadata variable: {0}'
    code = 410


@final
class EmptyModuleViolation(SimpleViolation):
    """
    Forbids to have empty modules.

    Reasoning:
        Why is it even there? Do not polute your project with empty files.

    Solution:
        If you have an empty module there are two ways to handle that:

        1. delete it
        2. drop some documentation in it, so you will explain why it is there

    .. versionadded:: 0.1.0

    """

    error_template = 'Found empty module'
    code = 411


@final
class InitModuleHasLogicViolation(SimpleViolation):
    """
    Forbids to have logic inside ``__init__`` module.

    Reasoning:
        If you have logic inside the ``__init__`` module
        it means several things:

        1. you are keeping some outdated stuff there, you need to refactor
        2. you are placing this logic into the wrong file,
           just create another one
        3. you are doing some dark magic, and you should not do that

    Solution:
        Put your code in other modules.

    However, we allow to have some contents inside the ``__init__`` module:

    1. comments, since they are dropped before AST comes in play
    2. docs string, because sometimes it is required to state something

    It is also fine when you have different users that use your code.
    And you do not want to break everything for them.
    In this case this rule can be configured.

    Configuration:
        This rule is configurable with ``--i-control-code``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found `__init__.py` module with logic'
    code = 412


# Modules:

@final
class WrongKeywordViolation(ASTViolation):
    """
    Forbids to use some keywords from ``python``.

    Reasoning:
        We believe that some keywords are anti-patterns.
        They promote bad-practices like ``global`` and ``pass``,
        or just not user-friendly like ``del``.

    Solution:
        Solutions differ from keyword to keyword.
        ``pass`` should be replaced with docstring or ``contextlib.suppress``.
        ``del`` should be replaced with specialized methods like ``.pop()``.
        ``global`` and ``nonlocal`` usages should be refactored.

    Example::

        # Wrong:
        pass
        del
        nonlocal
        global

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong keyword: {0}'
    code = 420


@final
class WrongFunctionCallViolation(ASTViolation):
    """
    Forbids to call some built-in functions.

    Reasoning:
        Some functions are only suitable
        for very specific use cases,
        we forbid to use them in a free manner.

    See
    :py:data:`~wemake_python_styleguide.constants.FUNCTIONS_BLACKLIST`
    for the full list of blacklisted functions.

    See also:
        https://www.youtube.com/watch?v=YjHsOrOOSuI

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong function call: {0}'
    code = 421


@final
class FutureImportViolation(ASTViolation):
    """
    Forbids to use ``__future__`` imports.

    Reasoning:
        Almost all ``__future__`` imports are legacy ``python2`` compatibility
        tools that are no longer required.

    Solution:
        Remove them. Drop ``python2`` support.

    Except, there are some new ones for ``python4`` support.
    See
    :py:data:`~wemake_python_styleguide.constants.FUTURE_IMPORTS_WHITELIST`
    for the full list of allowed future imports.

    Example::

        # Correct:
        from __future__ import annotations

        # Wrong:
        from __future__ import print_function

    .. versionadded:: 0.1.0

    """

    error_template = 'Found future import: {0}'
    code = 422


@final
class RaiseNotImplementedViolation(ASTViolation):
    """
    Forbids to use ``NotImplemented`` error.

    Reasoning:
        These two violations look so similar.
        But, these violations have different use cases.
        Use cases of ``NotImplemented`` is too limited
        to be generally available.

    Solution:
        Use ``NotImplementedError``.

    Example::

        # Correct:
        raise NotImplementedError('To be done')

        # Wrong:
        raise NotImplemented

    .. versionadded:: 0.1.0

    See Also:
        https://stackoverflow.com/a/44575926/4842742

    """

    error_template = 'Found raise NotImplemented'
    code = 423


@final
class BaseExceptionViolation(ASTViolation):
    """
    Forbids to use ``BaseException`` exception.

    Reasoning:
        We can silence system exit and keyboard interrupt with this exception
        handler. It is almost the same as raw ``except:`` block.

    Solution:
        Handle ``Exception``, ``KeyboardInterrupt``,
        ``GeneratorExit``, and ``SystemExit`` separately.
        Do not use the plain ``except:`` keyword.

    Example::

        # Correct:
        except Exception as ex: ...

        # Wrong:
        except BaseException as ex: ...

    .. versionadded:: 0.3.0

    See Also:
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        https://help.semmle.com/wiki/pages/viewpage.action?pageId=1608527

    """

    error_template = 'Found except `BaseException`'
    code = 424


@final
class BooleanPositionalArgumentViolation(ASTViolation):
    """
    Forbids to pass booleans as non-keyword parameters.

    Reasoning:
        Passing boolean as regular positional
        parameters is very non-descriptive.
        It is almost impossible to tell, what does this parameter means.
        And you almost always have to look up the implementation to tell
        what is going on.

    Solution:
        Pass booleans as keywords only.
        This will help you to save extra context on what's going on.

    Example::

        # Correct:
        UsersRepository.update(cache=True)

        # Wrong:
        UsersRepository.update(True)

    .. versionadded:: 0.6.0

    """

    error_template = 'Found boolean non-keyword argument'
    code = 425


# Design:

@final
class NestedFunctionViolation(ASTViolation):
    """
    Forbids to have nested functions.

    Reasoning:
        Nesting functions is a bad practice.
        It is hard to test them, it is hard then to separate them.
        People tend to overuse closures, so it's hard to manage the dataflow.

    Solution:
        Just write flat functions, there's no need to nest them.
        Pass parameters as normal arguments, do not use closures.
        Until you need them for decorators or factories.

    We also disallow to nest ``lambda`` and ``async`` functions.

    See
    :py:data:`~wemake_python_styleguide.constants.NESTED_FUNCTIONS_WHITELIST`
    for the whole list of whitelisted names.

    Example::

        # Correct:
        def do_some(): ...
        def other(): ...

        # Wrong:
        def do_some():
            def inner():
                ...

    .. versionadded:: 0.1.0

    """

    error_template = 'Found nested function: {0}'
    code = 430


@final
class NestedClassViolation(ASTViolation):
    """
    Forbids to use nested classes.

    Reasoning:
        Nested classes are really hard to manage.
        You can not even create an instance of this class in many cases.
        Testing them is also really hard.

    Solution:
        Just write flat classes, there's no need nest them.
        If you are nesting classes inside a function for parametrization,
        then you will probably need to use different design (or metaclasses).

    See
    :py:data:`~wemake_python_styleguide.constants.NESTED_CLASSES_WHITELIST`
    for the full list of whitelisted names.

    Example::

        # Correct:
        class Some(object): ...
        class Other(object): ...

        # Wrong:
        class Some(object):
            class Inner(object):
                ...

    .. versionadded:: 0.1.0

    """

    error_template = 'Found nested class: {0}'
    code = 431


@final
class MagicNumberViolation(ASTViolation):
    """
    Forbids to use magic numbers in your code.

    What we call a "magic number"? Well, it is actually any number that
    appears in your code out of nowhere. Like ``42``. Or ``0.32``.

    Reasoning:
        It is very hard to remember what these numbers actually mean.
        Why were they used? Should they ever be changed?
        Or are they eternal like ``3.14``?

    Solution:
        Give these numbers a name! Move them to a separate variable,
        giving more context to the reader. And by moving things into new
        variables you will trigger other complexity checks.

    Example::

        # Correct:
        price_in_euro = 3.33  # could be changed later
        total = get_items_from_cart() * price_in_euro

        # Wrong:
        total = get_items_from_cart() * 3.33

    What are numbers that we exclude from this check?
    Any numbers that are assigned to a variable, array, dictionary,
    or keyword arguments inside a function.
    ``int`` numbers that are in range ``[-10, 10]`` and
    some other common numbers, that are defined in
    :py:data:`~wemake_python_styleguide.constants.MAGIC_NUMBERS_WHITELIST`

    .. versionadded:: 0.1.0

    See also:
        https://en.wikipedia.org/wiki/Magic_number_(programming)

    """

    code = 432
    error_template = 'Found magic number: {0}'


@final
class StaticMethodViolation(ASTViolation):
    """
    Forbids to use ``@staticmethod`` decorator.

    Reasoning:
        Static methods are not required to be inside the class.
        Because they even do not have access to the current instance.

    Solution:
        Use instance methods, ``@classmethod``, or functions instead.

    .. versionadded:: 0.1.0

    """

    error_template = 'Found using `@staticmethod`'
    code = 433


@final
class BadMagicMethodViolation(ASTViolation):
    """
    Forbids to use some magic methods.

    Reasoning:
        We forbid to use magic methods related to the forbidden language parts.
        Likewise, we forbid to use ``del`` keyword, so we forbid to use all
        magic methods related to it.

    Solution:
        Refactor you code to use custom methods instead.
        It will give more context to your app.

    See
    :py:data:`~wemake_python_styleguide.constants.MAGIC_METHODS_BLACKLIST`
    for the full blacklist of the magic methods.

    .. versionadded:: 0.1.0

    See also:
        https://www.youtube.com/watch?v=F6u5rhUQ6dU

    """

    error_template = 'Found using restricted magic method: {0}'
    code = 434


@final
class NestedImportViolation(ASTViolation):
    """
    Forbids to have nested imports in functions.

    Reasoning:
        Usually nested imports are used to fix the import cycle.
        So, nested imports show that there's an issue with you design.

    Solution:
        You don't need nested imports, you need to refactor your code.
        Introduce a new module or find another way to do what you want to do.
        Rethink how your layered architecture should look like.

    Example::

        # Correct:
        from my_module import some_function

        def some(): ...

        # Wrong:
        def some():
            from my_module import some_function

    .. versionadded:: 0.1.0

    See also:
        https://github.com/seddonym/layer_linter

    """

    error_template = 'Found nested import'
    code = 435


@final
class RedundantLoopElseViolation(ASTViolation):
    """
    Forbids to use ``else`` without ``break`` in a loop.

    We use the same logic for ``for`` and ``while`` loops.

    Reasoning:
        When there's no ``break`` keyword in loop's body it means
        that ``else`` will always be called.
        This rule will reduce complexity, improve readability,
        and protect from possible errors.

    Solution:
        Refactor your ``else`` case logic to be inside the loop's body.
        Or right after it.

    Example::

        # Correct:
        for letter in 'abc':
            if letter == 'b':
                break
        else:
            print('"b" is not found')

        for letter in 'abc':
            print(letter)
        print('always called')

        # Wrong:
        for letter in 'abc':
            print(letter)
        else:
            print('always called')

    .. versionadded:: 0.3.0

    """

    error_template = 'Found `else` in a loop without `break`'
    code = 436


@final
class RedundantFinallyViolation(ASTViolation):
    """
    Forbids to use ``finally`` in ``try`` block without ``except`` block.

    Reasoning:
        This rule will reduce complexity and improve readability.

    Solution:
        Refactor your ``try`` logic.
        Replace the ``try-finally`` statement with a ``with`` statement.

    Example::

        # Correct:
        with open("filename") as f:
            f.write(...)

        # Wrong:
        try:
            f = open("filename")
            f.write(...)
        finally:
            f.close()

    .. versionadded:: 0.3.0

    """

    error_template = 'Found `finally` in `try` block without `except`'
    code = 437


@final
class ReassigningVariableToItselfViolation(ASTViolation):
    """
    Forbids to assign variable to itself.

    Reasoning:
        There is no need to do that.
        Generally it is an indication of some error or just dead code.

    Example::

        # Correct:
        some = some + 1
        x_coord, y_coord = y_coord, x_coord

        # Wrong:
        some = some
        x_coord, y_coord = x_coord, y_coord

    .. versionadded:: 0.3.0

    """

    error_template = 'Found reassigning variable to itself'
    code = 438


@final
class YieldInsideInitViolation(ASTViolation):
    """
    Forbids to use ``yield`` inside of ``__init__`` method.

    Reasoning:
        ``__init__`` should be used to initialize new objects.
        It shouldn't ``yield`` anything, because it should return ``None``
        by the convention.

    Example::

         # Correct:
        class Example(object):
            def __init__(self):
                self._public_items_count = 0

        # Wrong:
        class Example(object):
            def __init__(self):
                yield 10

    .. versionadded:: 0.3.0

    """

    error_template = 'Found `yield` inside `__init__` method'
    code = 439


@final
class ProtectedModuleViolation(ASTViolation):
    """
    Forbids to import protected modules.

    Reasoning:
        When importing protected modules we break a contract
        that authors of this module enforce.
        This way we are not respecting encapsulation and it may break
        our code at any moment.

    Solution:
        Do not import anything from protected modules.
        Respect the encapsulation.

    Example::

        # Correct:
        from some.public.module import FooClass

        # Wrong:
        import _compat
        from some._protected.module import BarClass
        from some.module import _protected

    .. versionadded:: 0.3.0

    """

    error_template = 'Found protected module import'
    code = 440


@final
class ProtectedAttributeViolation(ASTViolation):
    """
    Forbids to use protected attributes and methods.

    Reasoning:
        When using protected attributes and method we break a contract
        that authors of this class enforce.
        This way we are not respecting encapsulation and it may break
        our code at any moment.

    Solution:
        Do not use protected attributes and methods.
        Respect the encapsulation.

    Example::

        # Correct:
        self._protected = 1
        cls._hidden_method()
        some.public()

        # Wrong:
        print(some._protected)
        instance._hidden()
        self.container._internal = 10

    Note, that it is possible to use protected attributes with ``self``
    and ``cls`` as base names. We allow this so you can create and use
    protected attributes and methods inside the class context.
    This is how protected attributes should be used.

    .. versionadded:: 0.3.0

    """

    error_template = 'Found protected attribute usage: {0}'
    code = 441


@final
class LambdaInsideLoopViolation(ASTViolation):
    """
    Forbids to use ``lambda`` inside loops.

    Reasoning:
        It is error-prone to use ``lambda`` inside
        ``for`` and ``while`` loops due to the famous late-binding.

    Solution:
        Use regular functions, factory functions, or ``partial`` functions.
        Save yourself from possible confusion.

    Example::

        # Correct:
        for index in range(10):
            some.append(partial_function(index))

        # Wrong:
        for index in range(10):
            some.append(lambda index=index: index * 10))
            other.append(lambda: index * 10))

    .. versionadded:: 0.5.0

    See also:
        https://docs.python-guide.org/writing/gotchas/#late-binding-closures

    """

    error_template = "Found `lambda` in loop's body"
    code = 442


@final
class UnreachableCodeViolation(ASTViolation):
    """
    Forbids to have unreachable code.

    What is unreachable code? It is some lines of code that
    can not be executed by python's interpreter.

    This is probably caused by ``return`` or ``raise`` statements.
    However, we can not cover 100% of truly unreachable code by this rule.
    This happens due to the dynamic nature of python.
    For example, detecting that ``1 / some_value`` would sometimes raise
    an exception is too complicated and is out of scope of this rule.

    Reasoning:
        Having dead code in your project is an indicator that you
        do not care about your code base at all.
        It dramatically reduces code quality and readability.
        It also demotivates team members.

    Solution:
        Delete any unreachable code your have.
        Or refactor it, if this happens by your mistake.

    Example::

        # Correct:
        def some_function():
            print('This line is reachable, all good')
            return 5

        # Wrong:
        def some_function():
            return 5
            print('This line is unreachable')

    .. versionadded:: 0.5.0

    """

    error_template = 'Found unreachable code'
    code = 443


@final
class StatementHasNoEffectViolation(ASTViolation):
    """
    Forbids to have statements that do nothing.

    Reasoning:
        Statements that just access the value,
        or expressions used as statements indicate that your code
        contains dead lines. They just pollute your codebase and do nothing.

    Solution:
        Refactor your code in case it was a typo or error.
        Or just delete this code.

    Example::

        # Correct:
        def some_function():
            price = 8 + 2
            return price

        # Wrong:
        def some_function():
            8 + 2
            print

    .. versionadded:: 0.5.0

    """

    error_template = 'Found statement that has no effect'
    code = 444


@final
class MultipleAssignmentsViolation(ASTViolation):
    """
    Forbids to have statements that do nothing.

    Reasoning:
        Multiple assignments on the same line might not do what you think
        they do. They can also grown pretty long. And you will not notice
        the rising complexity of your code.

    Solution:
        Use separate lines for each assignment.

    Example::

        # Correct:
        a = 1
        b = 1

        # Wrong:
        a = b = 1

    .. versionadded:: 0.6.0

    """

    error_template = 'Found multiple assign targets'
    code = 445


@final
class IncorrectUnpackingViolation(ASTViolation):
    """
    Forbids to have statements that do nothing.

    Reasoning:
        Having unpacking with side-effects is very dirty.
        You might get in serious and very hard-to-debug troubles because of
        this technique. So, do not use it.

    Solution:
        Use unpacking with only variables, not any other entities.

    Example::

        # Correct:
        first, second = some()

        # Wrong:
        first, some_dict['alias'] = some()

    .. versionadded:: 0.6.0

    """

    error_template = 'Found incorrect unpacking target'
    code = 446


@final
class DuplicateExceptionViolation(ASTViolation):
    """
    Forbids to have the same exception class in multiple ``except`` blocks.

    Reasoning:
        Having the same exception name in different blocks means
        that something is not right: since only one branch will work.
        Other one will always be ignored. So, that is clearly an error.

    Solution:
        Use unique exception handling rules.

    Example::

        # Correct:
        try:
            ...
        except ValueError:
            ...

        # Wrong:
        try:
            ...
        except ValueError:
            ...
        except ValueError:
            ...

    .. versionadded:: 0.6.0

    """

    error_template = 'Found duplicate exception: {0}'
    code = 447
