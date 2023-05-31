"""
These checks ensure that you follow the best practices.

The source for these best practices is countless hours
we have spent debugging software or reviewing it.

How do we find inspiration for new rules?
We find some ugly code during code reviews and audits,
then we forbid the use of code like it forever.

.. currentmodule:: wemake_python_styleguide.violations.best_practices

Summary
-------

.. autosummary::
   :nosignatures:

   WrongMagicCommentViolation
   WrongDocCommentViolation
   OveruseOfNoqaCommentViolation
   OveruseOfNoCoverCommentViolation
   ComplexDefaultValueViolation
   LoopVariableDefinitionViolation
   ContextManagerVariableDefinitionViolation
   MutableModuleConstantViolation
   SameElementsInConditionViolation
   HeterogeneousCompareViolation
   WrongModuleMetadataViolation
   EmptyModuleViolation
   InitModuleHasLogicViolation
   BadMagicModuleFunctionViolation
   WrongUnpackingViolation
   DuplicateExceptionViolation
   YieldInComprehensionViolation
   NonUniqueItemsInHashViolation
   BaseExceptionSubclassViolation
   TryExceptMultipleReturnPathViolation
   WrongKeywordViolation
   WrongFunctionCallViolation
   FutureImportViolation
   RaiseNotImplementedViolation
   BaseExceptionViolation
   BooleanPositionalArgumentViolation
   LambdaInsideLoopViolation
   UnreachableCodeViolation
   StatementHasNoEffectViolation
   MultipleAssignmentsViolation
   NestedFunctionViolation
   NestedClassViolation
   MagicNumberViolation
   NestedImportViolation
   ReassigningVariableToItselfViolation
   ListMultiplyViolation
   ProtectedModuleViolation
   ProtectedAttributeViolation
   StopIterationInsideGeneratorViolation
   WrongUnicodeEscapeViolation
   BlockAndLocalOverlapViolation
   ControlVarUsedAfterBlockViolation
   OuterScopeShadowingViolation
   UnhashableTypeInHashViolation
   WrongKeywordConditionViolation
   WrongNamedKeywordViolation
   ApproximateConstantViolation
   StringConstantRedefinedViolation
   IncorrectExceptOrderViolation
   FloatKeyViolation
   ProtectedModuleMemberViolation
   PositionalOnlyArgumentsViolation
   LoopControlFinallyViolation
   ShebangViolation
   BaseExceptionRaiseViolation
   NonTrivialExceptViolation
   FloatingNanViolation
   InfiniteWhileLoopViolation
   ImportCollisionViolation
   FloatComplexCompareViolation
   SingleElementDestructuringViolation
   ForbiddenInlineIgnoreViolation
   WrongMultilineStringUseViolation
   GetterWithoutReturnViolation
   EmptyCommentViolation
   BitwiseAndBooleanMixupViolation
   NewStyledDecoratorViolation
   BareRaiseViolation
   RedundantEnumerateViolation
   RaiseFromItselfViolation
   KwargsUnpackingInClassDefinitionViolation
   ConsecutiveSlicesViolation
   GettingElementByUnpackingViolation
   WrongEmptyLinesCountViolation

Best practices
--------------

.. autoclass:: WrongMagicCommentViolation
.. autoclass:: WrongDocCommentViolation
.. autoclass:: OveruseOfNoqaCommentViolation
.. autoclass:: OveruseOfNoCoverCommentViolation
.. autoclass:: ComplexDefaultValueViolation
.. autoclass:: LoopVariableDefinitionViolation
.. autoclass:: ContextManagerVariableDefinitionViolation
.. autoclass:: MutableModuleConstantViolation
.. autoclass:: SameElementsInConditionViolation
.. autoclass:: HeterogeneousCompareViolation
.. autoclass:: WrongModuleMetadataViolation
.. autoclass:: EmptyModuleViolation
.. autoclass:: InitModuleHasLogicViolation
.. autoclass:: BadMagicModuleFunctionViolation
.. autoclass:: WrongUnpackingViolation
.. autoclass:: DuplicateExceptionViolation
.. autoclass:: YieldInComprehensionViolation
.. autoclass:: NonUniqueItemsInHashViolation
.. autoclass:: BaseExceptionSubclassViolation
.. autoclass:: TryExceptMultipleReturnPathViolation
.. autoclass:: WrongKeywordViolation
.. autoclass:: WrongFunctionCallViolation
.. autoclass:: FutureImportViolation
.. autoclass:: RaiseNotImplementedViolation
.. autoclass:: BaseExceptionViolation
.. autoclass:: BooleanPositionalArgumentViolation
.. autoclass:: LambdaInsideLoopViolation
.. autoclass:: UnreachableCodeViolation
.. autoclass:: StatementHasNoEffectViolation
.. autoclass:: MultipleAssignmentsViolation
.. autoclass:: NestedFunctionViolation
.. autoclass:: NestedClassViolation
.. autoclass:: MagicNumberViolation
.. autoclass:: NestedImportViolation
.. autoclass:: ReassigningVariableToItselfViolation
.. autoclass:: ListMultiplyViolation
.. autoclass:: ProtectedModuleViolation
.. autoclass:: ProtectedAttributeViolation
.. autoclass:: StopIterationInsideGeneratorViolation
.. autoclass:: WrongUnicodeEscapeViolation
.. autoclass:: BlockAndLocalOverlapViolation
.. autoclass:: ControlVarUsedAfterBlockViolation
.. autoclass:: OuterScopeShadowingViolation
.. autoclass:: UnhashableTypeInHashViolation
.. autoclass:: WrongKeywordConditionViolation
.. autoclass:: WrongNamedKeywordViolation
.. autoclass:: ApproximateConstantViolation
.. autoclass:: StringConstantRedefinedViolation
.. autoclass:: IncorrectExceptOrderViolation
.. autoclass:: FloatKeyViolation
.. autoclass:: ProtectedModuleMemberViolation
.. autoclass:: PositionalOnlyArgumentsViolation
.. autoclass:: LoopControlFinallyViolation
.. autoclass:: ShebangViolation
.. autoclass:: BaseExceptionRaiseViolation
.. autoclass:: NonTrivialExceptViolation
.. autoclass:: FloatingNanViolation
.. autoclass:: InfiniteWhileLoopViolation
.. autoclass:: ImportCollisionViolation
.. autoclass:: FloatComplexCompareViolation
.. autoclass:: SingleElementDestructuringViolation
.. autoclass:: ForbiddenInlineIgnoreViolation
.. autoclass:: WrongMultilineStringUseViolation
.. autoclass:: GetterWithoutReturnViolation
.. autoclass:: EmptyCommentViolation
.. autoclass:: BitwiseAndBooleanMixupViolation
.. autoclass:: NewStyledDecoratorViolation
.. autoclass:: BareRaiseViolation
.. autoclass:: RedundantEnumerateViolation
.. autoclass:: RaiseFromItselfViolation
.. autoclass:: KwargsUnpackingInClassDefinitionViolation
.. autoclass:: ConsecutiveSlicesViolation
.. autoclass:: GettingElementByUnpackingViolation
.. autoclass:: WrongEmptyLinesCountViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    SimpleViolation,
    TokenizeViolation,
)


@final
class WrongMagicCommentViolation(SimpleViolation):
    """
    Restrict various control (such as magic) comments.

    We do not allow:

    1. ``# noqa`` comment without specified violations
    2. ``# type: some_type`` comments to specify a type for ``typed_ast``

    This violation is reported at the top of the module,
    so it cannot be locally ignored.

    Reasoning:
        We cover several use-cases in a single rule.
        ``# noqa`` comment is restricted because it can hide other violations.
        ``# type: some_type`` comment is restricted because we can use type annotations instead.

    Solution:
        Use ``# noqa`` comments with specified error types.
        Use type annotations to specify types.

    We still allow using ``# type: ignore`` comment,
    since sometimes it is required.

    Example::

        # Correct:
        type = MyClass.get_type()  # noqa: WPS125
        coordinate: int = 10
        some.int_field = 'text'  # type: ignore

        number: int
        for number in some_untyped_iterable():
            ...

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
    Forbid empty doc comments (``#:``).

    Reasoning:
        Doc comments are used to provide documentation
        but supplying empty doc comments breaks this use-case.
        It is unclear why they can be used with no contents.

    Solution:
        Add some documentation to this comment or remove it.

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


@final
class OveruseOfNoqaCommentViolation(SimpleViolation):
    """
    Forbid too many ``# noqa`` comments.

    We count them on a per-module basis.

    Reasoning:
        Having too many ``# noqa`` comments makes your code
        less readable and indicates that there's something
        wrong with it.

    Solution:
        Refactor your code to match our style.
        Or use a config file to switch off some checks.

    Configuration:
        This rule is configurable with ``--max-noqa-comments``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_NOQA_COMMENTS`

    .. versionadded:: 0.7.0

    """

    error_template = 'Found `noqa` comments overuse: {0}'
    code = 402


@final
class OveruseOfNoCoverCommentViolation(SimpleViolation):
    """
    Forbid too many ``# pragma: no cover`` comments.

    We count them on a per-module basis.
    We use :str:`wemake_python_styleguide.constants.MAX_NO_COVER_COMMENTS`
    as a default value.

    Reasoning:
        Having too many ``# pragma: no cover`` comments
        indicates that there's something wrong with the code.
        Moreover, it makes your tests useless, since they do not cover
        a big portion of your code.

    Solution:
        Refactor your code to match the style.
        Or use a config file to switch off some checks.

    .. versionadded:: 0.8.0

    """

    error_template = 'Found `no cover` comments overuse: {0}'
    code = 403


@final
class ComplexDefaultValueViolation(ASTViolation):
    """
    Forbid complex defaults.

    Anything that is not a ``ast.Name``, ``ast.Attribute``, ``ast.Str``,
    ``ast.NameConstant``, ``ast.Tuple``, ``ast.Bytes``, ``ast.Num``
    or ``ast.Ellipsis`` should be moved out from defaults.

    Reasoning:
        It can be tricky. Nothing stops you from making database calls or HTTP
        requests in such expressions. It is also not readable for us.

    Solution:
        Move the expression out from default value.

    Example::

        # Correct:
        SHOULD_USE_DOCTEST = 'PYFLAKES_DOCTEST' in os.environ
        def __init__(self, with_doctest=SHOULD_USE_DOCTEST):

        # Wrong:
        def __init__(self, with_doctest='PYFLAKES_DOCTEST' in os.environ):

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found complex default value'
    code = 404
    previous_codes = {459}


@final
class LoopVariableDefinitionViolation(ASTViolation):
    """
    Forbid anything other than ``ast.Name`` to define loop variables.

    Reasoning:
        When defining a ``for`` loop with attributes, indexes, calls,
        or any other nodes it does dirty things inside.

    Solution:
        Use regular ``ast.Name`` variables.
        Or tuple of ``ast.Name`` variables.
        Star names are also fine.

    Example::

        # Correct:
        for person in database.people():
            ...

        # Wrong:
        for context['person'] in database.people():
            ...

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found wrong `for` loop variable definition'
    code = 405
    previous_codes = {460}


@final
class ContextManagerVariableDefinitionViolation(ASTViolation):
    """
    Forbid anything other than ``ast.Name`` to define contexts.

    Reasoning:
        When defining a ``with`` context managers with attributes,
        indexes, calls, or any other nodes it does dirty things inside.

    Solution:
        Use regular ``ast.Name`` variables.
        Or tuple of ``ast.Name`` variables.
        Star names are also fine.

    Example::

        # Correct:
        with open('README.md') as readme:
            ...

        # Wrong:
        with open('README.md') as files['readme']:
            ...

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found wrong context manager variable definition'
    code = 406
    previous_codes = {461}


@final
class MutableModuleConstantViolation(ASTViolation):
    """
    Forbid mutable constants on a module level.

    Reasoning:
        Constants should be immutable.

    Solution:
        Use immutable types for constants.

    We only treat ``ast.Set``, ``ast.Dict``, ``ast.List`` and comprehensions
    as mutable things. All other nodes are still fine.

    Example::

        # Correct:
        import types
        CONST1 = frozenset((1, 2, 3))
        CONST2 = (1, 2, 3)
        CONST3 = types.MappingProxyType({'key': 'value'})

        # Wrong:
        CONST1 = {1, 2, 3}
        CONST2 = [x for x in some()]
        CONST3 = {'key': 'value'}

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found mutable module constant'
    code = 407
    previous_codes = {466}


@final
class SameElementsInConditionViolation(ASTViolation):
    """
    Forbid using the same logical conditions in one expression.

    Reasoning:
        Using the same name in a logical condition more than once
        indicates that you are either making a logical mistake,
        or just over-complicating your design.

    Solution:
        Remove the duplicated condition.

    Example::

        # Correct:
        if some_value or other_value:
            ...

        # Wrong:
        if some_value or some_value:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.13.0

    """

    error_template = 'Found duplicate logical condition'
    code = 408
    previous_codes = {469}


@final
class HeterogeneousCompareViolation(ASTViolation):
    """
    Forbid heterogeneous operators in one comparison.

    Note, that we do allow mixing  ``>`` with ``>=``
    and ``<`` with ``<=`` operators.

    Reasoning:
        This is hard to read and understand.

    Solution:
        Refactor the expression to have separate parts
        joined with ``and`` boolean operator.

    Example::

        # Correct:
        if x == y == z:
            ...

        if x > y >= z:
            ...

        # Wrong:
        if x > y == 5:
            ...

        if x == y != z:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found heterogeneous compare'
    code = 409
    previous_codes = {471}


@final
class WrongModuleMetadataViolation(ASTViolation):
    """
    Forbid some module-level variables.

    Reasoning:
        We discourage using module variables like ``__author__``,
        because code should not contain any metadata.

    Solution:
        Place all the metadata in ``setup.py``,
        ``setup.cfg``, or ``pyproject.toml``.
        Use proper docstrings and packaging classifiers.
        Use ``importlib.metadata``
        if you need to import this data into your app.

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
    Forbid empty modules.

    Reasoning:
        Why is it even there? Do not pollute your project with empty files.

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
    Forbid logic inside ``__init__`` module.

    Reasoning:
        If you have logic inside the ``__init__`` module
        It means several things:

        1. you are keeping some outdated stuff there, you need to refactor
        2. you are placing this logic in the wrong file,
           just create another one
        3. you are doing some dark magic, and you should not do that

    Solution:
        Put your code in other modules.

    However, we allow some contents inside the ``__init__`` module:

    1. comments, since they are dropped before AST comes in play
    2. docstrings are used sometimes when required to state something

    It is also fine when you have different users that use your code.
    And you do not want to break everything for them.
    In this case, this rule can be configured.

    Configuration:
        This rule is configurable with ``--i-control-code``
        and ``--i-dont-control-code``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`

    When using ``--i-dont-control-code`` it is still recommended
    to only have imports in your ``__init__.py``.

    .. versionadded:: 0.1.0

    """

    error_template = 'Found `__init__.py` module with logic'
    code = 412


@final
class BadMagicModuleFunctionViolation(ASTViolation):
    """
    Forbid ``__getattr__`` and ``__dir__`` module magic methods.

    Reasoning:
        It does not bring any features,
        only making it harder to understand what is going on.

    Solution:
        Refactor your code to use custom methods instead.

    Configuration:
        This rule is configurable with ``--i-control-code``
        and ``--i-dont-control-code``.
    Default:
        :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`

    .. versionadded:: 0.9.0

    """

    error_template = 'Found bad magic module function: {0}'
    code = 413


@final
class WrongUnpackingViolation(ASTViolation):
    """
    Forbid tuple unpacking with side-effects.

    Reasoning:
        Having unpacking with side-effects is very dirty.
        You might get in serious and very hard-to-debug troubles because of
        this technique so do not use it.

        This includes assigning to attributes, as this results in modifying
        the instance. Every modification should be explicit on it's own line.

    Solution:
        Use unpacking only with variables, not any other entities.

    Example::

        # Correct:
        reader, writer = call()
        self.reader = reader
        self.writer = writer

        # Wrong:
        first, some_dict['alias'] = some()
        self.reader, self.writer = call()

    .. versionadded:: 0.6.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found incorrect unpacking target'
    code = 414
    previous_codes = {446}


@final
class DuplicateExceptionViolation(ASTViolation):
    """
    Forbid the same exception class in multiple ``except`` blocks.

    Reasoning:
        Having the same exception name in different blocks means
        that something is not right: since only one branch will work.
        Another one will always be ignored. So, that is an error.

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
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found duplicate exception: {0}'
    code = 415
    previous_codes = {447}


@final
class YieldInComprehensionViolation(ASTViolation):
    """
    Forbid ``yield`` keyword inside comprehensions.

    This is a ``SyntaxError`` starting from ``python3.8``.

    Reasoning:
        Having the ``yield`` keyword inside comprehensions is error-prone.
        You can shoot yourself in the foot by
        an inaccurate usage of this feature.

    Solution:
        Use regular ``for`` loops with ``yield`` keywords
        or create a separate generator function.

    Example::

        # Wrong:
        list((yield letter) for letter in 'ab')
        # Will resilt in: ['a', None, 'b', None]

        list([(yield letter) for letter in 'ab'])
        # Will result in: ['a', 'b']

    See also:
        https://github.com/satwikkansal/wtfPython#-yielding-none

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.18.0
       No longer produced, kept here for historic reasons.

    """

    error_template = 'Found `yield` inside comprehension'
    code = 416
    previous_codes = {448}


@final
class NonUniqueItemsInHashViolation(ASTViolation):
    """
    Forbid duplicate items in hashes.

    Reasoning:
        When you explicitly put duplicate items
        in ``set`` literals or in ``dict`` keys
        it just does not make any sense since hashes cannot contain
        duplicate items and they will be removed anyway.

    Solution:
        Remove duplicate items.

    Example::

        # Correct:
        some_set = {'a', variable1}
        some_set = {make_call(), make_call()}

        # Wrong:
        some_set = {'a', 'a', variable1, variable1}

    Things that we consider duplicates: builtins and variables.
    These nodes are not checked because they may return different results:

    - function and method calls
    - comprehensions
    - attributes
    - subscribe operations

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.12.0

    """

    error_template = 'Found non-unique item in hash: {0}'
    code = 417
    previous_codes = {449}


@final
class BaseExceptionSubclassViolation(ASTViolation):
    """
    Forbid exceptions inherited from ``BaseException``.

    Reasoning:
        ``BaseException`` is a special case:
        it is not designed to be extended by users.
        A lot of your ``except Exception`` cases won't work.
        That's incorrect and dangerous.

    Solution:
        Change the base class to ``Exception``.

    Example::

        # Correct:
        class MyException(Exception):
            ...

        # Wrong:
        class MyException(BaseException):
            ...

    See also:
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found exception inherited from `BaseException`'
    code = 418
    previous_codes = {450}


@final
class TryExceptMultipleReturnPathViolation(ASTViolation):
    """
    Forbid multiple returning paths with ``try`` / ``except`` case.

    Note, that we check for any ``return``, ``break``, or ``raise`` nodes.

    Reasoning:
        The problem with ``return`` in ``else`` and ``finally``
        is that it is impossible to say what value is going to be
        returned without looking up the implementation details. Why?
        Because ``return`` does not expect
        that some other code will be executed after it.
        But, ``finally`` is always executed, even after ``return``.
        And ``else`` will not be executed when there are no exceptions
        in ``try`` case and a ``return`` statement.

    Solution:
        Remove ``return`` from one of the cases.

    Example::

        # Correct:
        try:
            return 1
        except YourException:
            ...
        finally:
            clear_things_up()

        # Wrong:
        try:
            return 1  # this line will never return
        except Exception:
            ...
        finally:
            return 2  # this line will actually return

        try:
            return 1  # this line will actually return
        except ZeroDivisionError:
            ...
        else:
            return 0  # this line will never return

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.12.0

    """

    error_template = 'Found `try`/`else`/`finally` with multiple return paths'
    code = 419
    previous_codes = {458}


@final
class WrongKeywordViolation(ASTViolation):
    """
    Forbid some ``python`` keywords.

    Reasoning:
        Using some keywords generally causes more pain than it relieves.

        ``del`` keyword is not composable with other functions,
        you cannot pass it as a regular function.
        It is also quite error-prone due to ``__del__`` magic method complexity
        and that ``del`` is actually used to nullify variables and delete them
        from the execution scope.
        Moreover, it has a lot of substitutions. You won't miss it!

        ``pass`` keyword is just useless by design. There's no use-case for it.
        Because it does literally nothing.

        ``global`` and ``nonlocal`` promote bad-practices of having an external
        mutable state somewhere. This solution does not scale
        and leads to multiple possible mistakes in the future.

    Solution:
        Solutions differ from keyword to keyword.
        ``pass`` should be replaced with docstring or ``contextlib.suppress``.
        ``del`` should be replaced with specialized methods like ``.pop()``.
        ``global`` and ``nonlocal`` usages should be refactored.

    .. versionadded:: 0.1.0

    """

    error_template = 'Found wrong keyword: {0}'
    code = 420


@final
class WrongFunctionCallViolation(ASTViolation):
    """
    Forbid calling some built-in functions.

    Reasoning:
        Some functions are only suitable
        for very specific use cases,
        we forbid the use of them in a free manner.

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
    Forbid ``__future__`` imports.

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
    Forbid ``NotImplemented`` exception.

    Reasoning:
        ``NotImplemented`` and ``NotImplementedError`` look similar
        but they have different use cases.
        Use cases of ``NotImplemented`` are too limited
        to be generally available.

    Solution:
        Use ``NotImplementedError``.

    Example::

        # Correct:
        raise NotImplementedError('To be done')

        # Wrong:
        raise NotImplemented

    .. versionadded:: 0.1.0

    See also:
        https://stackoverflow.com/a/44575926/4842742

    """

    error_template = 'Found raise NotImplemented'
    code = 423


@final
class BaseExceptionViolation(ASTViolation):
    """
    Forbid ``BaseException`` exception.

    Reasoning:
        We can silence system exit and keyboard interrupt
        with this exception handler.
        It is almost the same as raw ``except:`` block.

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

    See also:
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        https://help.semmle.com/wiki/pages/viewpage.action?pageId=1608527

    """

    error_template = 'Found except `BaseException`'
    code = 424


@final
class BooleanPositionalArgumentViolation(ASTViolation):
    """
    Forbid booleans as non-keyword parameters.

    Reasoning:
        Passing booleans as regular positional parameters
        is very non-descriptive.
        It is almost impossible to tell what this
        parameter means and you almost always have to look up the implementation
        to tell what is going on.
        The only exception from this rule is passing a boolean as a
        non-keyword argument when it is the only passed argument.


    Solution:
        Pass booleans as keywords only.
        This will help you to save extra context on what's going on.

    Example::

        # Correct:
        UserRepository.update(True)
        UsersRepository.add(user, cache=True)

        # Wrong:
        UsersRepository.add(user, True)

    .. versionadded:: 0.6.0

    """

    error_template = 'Found boolean non-keyword argument: {0}'
    code = 425


@final
class LambdaInsideLoopViolation(ASTViolation):
    """
    Forbid ``lambda`` inside loops.

    We check ``while``, ``for``, and ``async for`` loop bodies.
    We also check comprehension value parts.

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
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.14.0

    See also:
        https://docs.python-guide.org/writing/gotchas/#late-binding-closures

    """

    error_template = "Found `lambda` in loop's body"
    code = 426
    previous_codes = {442}


@final
class UnreachableCodeViolation(ASTViolation):
    """
    Forbid unreachable code.

    What is unreachable code? It is some lines of code that
    cannot be executed by python's interpreter.

    This is probably caused by ``return`` or ``raise`` statements.
    However, we cannot cover 100% of truly unreachable code by this rule.
    This happens due to the dynamic nature of python.
    For example, detecting that ``1 / some_value`` would sometimes raise
    an exception is too complicated and is out of the scope of this rule.

    Reasoning:
        Having dead code in your project is an indicator that
        you do not care about your codebase at all.
        It dramatically reduces code quality and readability.
        It also demotivates team members.

    Solution:
        Delete any unreachable code you have or refactor it,
        if this happens by your mistake.

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
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found unreachable code'
    code = 427
    previous_codes = {443}


@final
class StatementHasNoEffectViolation(ASTViolation):
    """
    Forbid statements that do nothing.

    Reasoning:
        Statements that just access the value or expressions
        used as statements indicate that your code
        contains deadlines.
        They just pollute your codebase and do nothing.

    Solution:
        Refactor your code in case it was a typo or error
        or just delete this code.

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
    .. versionchanged:: 0.11.0
    """

    error_template = 'Found statement that has no effect'
    code = 428
    previous_codes = {444}


@final
class MultipleAssignmentsViolation(ASTViolation):
    """
    Forbid multiple assignments on the same line.

    Reasoning:
        Multiple assignments on the same line might not do what you think
        they do. They can also grow pretty long and you might not notice
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
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found multiple assign targets'
    code = 429
    previous_codes = {445}


@final
class NestedFunctionViolation(ASTViolation):
    """
    Forbid nested functions.

    Reasoning:
        Nesting functions is bad practice.
        It is hard to test them and it is hard to separate them later.
        People tend to overuse closures, so it's hard to manage the dataflow.

    Solution:
        Just write flat functions, there's no need to nest them.
        Pass parameters as normal arguments, do not use closures
        until you need them for decorators or factories.

    We also forbid nesting ``lambda`` and ``async`` functions.

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
    Forbid nested classes.

    Reasoning:
        Nested classes are really hard to manage.
        You cannot even create an instance of this class in many cases.
        Testing them is also really hard.

    Solution:
        Just write flat classes, there's no need to nest them.
        If you are nesting classes inside a function for parametrization,
        then you will probably need to use a different design (or metaclasses).

    Configuration:
        This rule is configurable with ``--nested-classes-whitelist``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.NESTED_CLASSES_WHITELIST`

    Example::

        # Correct:
        class Some(object): ...
        class Other(object): ...

        # Wrong:
        class Some(object):
            class Inner(object):
                ...

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.13.0

    """

    error_template = 'Found nested class: {0}'
    code = 431


@final
class MagicNumberViolation(ASTViolation):
    """
    Forbid magic numbers.

    What do we call a "magic number"? Well, it is actually any number that
    appears in your code out of nowhere. Like ``42``. Or ``0.32``.

    Reasoning:
        It is very hard to remember what these numbers mean.
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

    What are the numbers that we exclude from this check?
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
class NestedImportViolation(ASTViolation):
    """
    Forbid imports nested in functions.

    Reasoning:
        Usually, nested imports are used to fix the import cycle.
        So, nested imports show that there's an issue with your design.

    Solution:
        You don't need nested imports, you need to refactor your code.
        Introduce a new module or find another way to do what you want to do.
        Rethink how your layered architecture should look.

    Example::

        # Correct:
        from my_module import some_function

        def some(): ...

        # Wrong:
        def some():
            from my_module import some_function

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.11.0

    See also:
        https://github.com/seddonym/layer_linter

    """

    error_template = 'Found nested import'
    code = 433
    previous_codes = {435}


@final
class ReassigningVariableToItselfViolation(ASTViolation):
    """
    Forbid assigning a variable to itself.

    Reasoning:
        There is no need to do that.
        Generally, it is an indication of some errors or just dead code.

    Example::

        # Correct:
        some = some + 1
        x_coord, y_coord = y_coord, x_coord
        flag = not flag

        # Wrong:
        some = some
        x_coord, y_coord = x_coord, y_coord

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.16.0

    """

    error_template = 'Found reassigning variable to itself: {0}'
    code = 434
    previous_codes = {438}


@final
class ListMultiplyViolation(ASTViolation):
    """
    Forbid multiplying lists.

    Reasoning:
        When you multiply lists - it does not create new values,
        it creates references to the existing value.
        It is not what people mean in 99.9% of cases.

    Solution:
        Use list comprehension or loop instead.

    Example::

        # Wrong:
        my_list = [1, 2, 3] * 3

    See also:
        https://github.com/satwikkansal/wtfPython#-explanation-8

    .. versionadded:: 0.12.0

    """

    error_template = 'Found list multiply'
    code = 435


@final
class ProtectedModuleViolation(ASTViolation):
    """
    Forbid importing protected modules.

    Related to :class:`~ProtectedModuleMemberViolation`.

    Reasoning:
        When importing protected modules we break a contract
        that authors of this module enforce.
        This way we are not respecting encapsulation and it may break
        our code at any moment.

    Solution:
        Do not import protected modules.
        Respect the encapsulation.

    Example::

        # Correct:
        import public_module
        from some.public.module import FooClass

        # Wrong:
        import _compat
        from some._protected.module import BarClass

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found protected module import: {0}'
    code = 436
    previous_codes = {440}


@final
class ProtectedAttributeViolation(ASTViolation):
    """
    Forbid protected attributes and methods.

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
        super()._protected()

        # Wrong:
        print(some._protected)
        instance._hidden()
        self.container._internal = 10

    Note, that it is possible to use protected attributes with
    ``self``, ``cls``, and ``super()`` as base names.
    We allow this so you can create and
    use protected attributes and methods inside the class context.
    This is how protected attributes should be used.

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found protected attribute usage: {0}'
    code = 437
    previous_codes = {441}


@final
class StopIterationInsideGeneratorViolation(ASTViolation):
    """
    Forbid raising ``StopIteration`` inside generators.

    Reasoning:
        ``StopIteration`` should not be raised explicitly in generators.

    Solution:
        Use a return statement to get out of a generator.

    Example::

        # Correct:
        def some_generator():
            if some_value:
                return
            yield 1

        # Wrong:
        def some_generator():
            if some_value:
                raise StopIteration
            yield 1

    See also:
        https://docs.python.org/3/library/exceptions.html#StopIteration

    .. versionadded:: 0.12.0

    """

    error_template = 'Found `StopIteration` raising inside generator'
    code = 438


@final
class WrongUnicodeEscapeViolation(TokenizeViolation):
    r"""
    Forbid Unicode escape sequences in binary strings.

    Reasoning:
        Binary strings do not work with Unicode.
        Having Unicode escape characters in there means
        that you have an error in your code.

    Solution:
        Use regular strings when escaping Unicode strings.

    Example::

        # Correct:
        escaped = '\u0041'  # equals to 'A'

        # Wrong:
        escaped = b'\u0040'  # equals to b'\\u0040'

    .. versionadded:: 0.12.0

    """

    error_template = 'Found unicode escape in a binary string: {0}'
    code = 439


@final
class BlockAndLocalOverlapViolation(ASTViolation):
    """
    Forbid overlapping local and block variables.

    What we call local variables:

    1. Assigns and annotations
    2. Function arguments (they are local to the function body)

    What we call block variables:

    1. Imports
    2. Functions and async functions definitions
    3. Classes, methods, and async methods definitions
    4. For and async for loops variables
    5. Except for block exception aliases

    We allow local variables to overlap themselves,
    we forbid block variables to overlap themselves.

    Example::

        # Correct:
        my_value = 1
        my_value = my_value + 1

        # Wrong:
        import my_value
        my_value = 1  # overlaps with import

    See also:
        https://github.com/satwikkansal/wtfPython#-explanation-20

    .. versionadded:: 0.12.0

    """

    error_template = 'Found block variables overlap: {0}'
    code = 440


@final
class ControlVarUsedAfterBlockViolation(ASTViolation):
    """
    Forbid control variables after the block body.

    What we call block control variables:

    1. ``for`` loop unpacked variables
    2. ``with`` context variables

    Reasoning:
        Variables leaking from the blocks can damage your logic.
        It might not contain what you think they contain.

    Solution:
        Use names inside the scope they are defined.
        Create new functions to return values in case
        you need to use block variables: when searching for a value, etc.

    Example::

        # Correct:
        for my_item in collection:
            print(my_item)

        # Wrong:
        for my_item in collection:
            ...
        print(my_item)

    See also:
        https://github.com/satwikkansal/wtfPython#-explanation-32

    .. versionadded:: 0.12.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found control variable used after block: {0}'
    code = 441


@final
class OuterScopeShadowingViolation(ASTViolation):
    """
    Forbid shadowing variables from outer scopes.

    We check the function, method, and module scopes.
    While we do not check the class scope. Because class level constants
    are not available via regular name,
    and they are scope to ``ClassName.var_name``.

    Reasoning:
        Shadowing can lead you to a big pile of storage and unexpected bugs.


    Solution:
        Use different names and do not allow scoping.

    Example::

        # Correct:
        def test(): ...

        def other():
            test1 = 1

        # Wrong:
        def test(): ...

        def other():
            test = 1  # shadows `test()` function

    .. versionadded:: 0.12.0

    """

    error_template = 'Found outer scope names shadowing: {0}'
    code = 442


@final
class UnhashableTypeInHashViolation(ASTViolation):
    """
    Forbid explicit unhashable types of asset items and dict keys.

    Reasoning:
        This will resolve in ``TypeError`` in runtime.

    Solution:
        Use hashable types to define set items and dict keys.

    Example::

        # Correct:
        my_dict = {1: {}, (1, 2): [], (2, 3): {1, 2}}

        # Wrong:
        my_dict = {[1, 2]: [], {2, 3}: {1, 2}}

    .. versionadded:: 0.12.0

    """

    error_template = 'Found unhashable item'
    code = 443


@final
class WrongKeywordConditionViolation(ASTViolation):
    """
    Forbid explicit falsely-evaluated conditions with several keywords.

    We check:

    - ``ast.While``
    - ``ast.Assert``

    We do not check variables, attributes, calls, bool and bin operators, etc.
    We forbid constants and some expressions.

    Reasoning:
        Some conditions tell us that this node won't work correctly.
        So, we need to check if we can fix that.

    Solution:
        Remove the unreachable node, or change the condition item.

    Example::

        # Correct:
        assert some_variable

        while True:
            ...

        # Wrong:
        assert []

        while False:
            ...

    .. versionadded:: 0.12.0
    .. versionchanged:: 0.13.0

    """

    error_template = 'Found incorrect keyword condition'
    code = 444


@final
class WrongNamedKeywordViolation(ASTViolation):
    """
    Forbid incorrectly named keywords in starred dicts.

    Reasoning:
        Using the incorrect keywords in a starred dict.
        Eg.: ``print(**{'@': 1})``.

    Solution:
        Don't use incorrect identifiers as keywords.

    Example::

        # Correct:
        print(**{'end': '|'})

        # Wrong:
        print(**{'3end': '|'})

    .. versionadded:: 0.13.0

    """

    code = 445
    error_template = 'Found incorrectly named keyword in the starred dict'


@final
class ApproximateConstantViolation(ASTViolation):
    """
    Forbid approximate constants.

    Reasoning:
        Some constants are already defined.
        No need to write them again, use existing values.
        We just compare numbers as strings and raise this
        violation when they start with the same chars.

    Solution:
        Use pre-defined constants.

    Example::

        # Correct:
        from math import pi
        random_number = 3.15
        too_short = 3.1

        # Wrong:
        pi = 3.14

    See
    :py:data:`~wemake_python_styleguide.constants.MATH_APPROXIMATE_CONSTANTS`
    for full list of math constants that we check for.

    See also:
        https://docs.python.org/3/library/math.html#constants

    .. versionadded:: 0.13.0

    """

    code = 446
    error_template = 'Found approximate constant: {0}'


@final
class StringConstantRedefinedViolation(ASTViolation):
    """
    Forbid using the alphabet as a string.

    Reasoning:
        Some constants are already defined.
        No need to write to them again, use existing values.
        We just compare strings and raise this violation
        when they have the same chars.

    Solution:
        Use pre-defined constants.

    Example::

        # Correct:
        import string
        UPPERCASE_ALPH = string.ascii_uppercase
        LOWERCASE_ALPH = string.ascii_lowercase

        # Wrong:
        GUESS_MY_NAME = "abcde...WXYZ"
        UPPERCASE_ALPH = "ABCD...WXYZ"
        LOWERCASE_ALPH = "abcd...wxyz"

    .. versionadded:: 0.13.0

    """

    error_template = 'Found alphabet as strings: {0}'
    code = 447


@final
class IncorrectExceptOrderViolation(ASTViolation):
    """
    Forbid incorrect order of ``except``.

    Note, we only check for built-in exceptions
    because we cannot statically identify
    the inheritance order of custom ones.

    Reasoning:
        Using incorrect order of exceptions is error-prone, since
        you end up with some unreachable exception clauses.

    Solution:
        Use the correct order of exceptions.

    Example::

        # Correct:
        try:
            ...
        except ValueError:
            ...
        except Exception:
            ...

        # Wrong:
        try:
            ...
        except Exception:
            ...
        except ValueError:
            ...

    See also:
        https://bit.ly/36MHlzw

    .. versionadded:: 0.13.0

    """

    error_template = 'Found incorrect exception order'
    code = 448


@final
class FloatKeyViolation(ASTViolation):
    """
    Forbid ``float`` keys.

    Reasoning:
        ``float`` is a very ugly data type.
        It has a lot of "precision" errors.
        When we use ``float`` as keys we can hit this wall.
        Moreover, we cannot use ``float`` keys with lists, by design.

    Solution:
        Use other data types: integers, decimals, or use fuzzy logic.

    Example::

        # Correct:
        some = {1: 'a'}
        some[1]

        # Wrong:
        some = {1.0: 'a'}
        some[1.0]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found float used as a key'
    code = 449


@final
class ProtectedModuleMemberViolation(ASTViolation):
    """
    Forbid importing protected objects from modules.

    Related to :class:`~ProtectedModuleViolation`.

    Reasoning:
        When importing a protected modules' members, we break the contract
        which the authors of this module enforce.
        By disrespecting encapsulation, we may break the code at any moment.

    Solution:
        Do not import protected objects from modules.
        Respect the encapsulation.

    Example::

        # Correct:
        from some.public.module import FooClass

        # Wrong:
        from some.module import _protected
        from some.module import _protected as not_protected

    .. versionadded:: 0.14.0

    """

    error_template = 'Found protected object import: {0}'
    code = 450


@final
class PositionalOnlyArgumentsViolation(ASTViolation):
    """
    Forbid positional only or ``/`` arguments.

    This violation is only raised for ``python3.8+``,
    earlier versions do not have this concept.

    Reasoning:
        This is a very rare case.
        Almost exclusively used by C code and stdlib.
        There's no point in declaring your own parameters as positional only.
        It will break your code!

    Solution:
        Use regular arguments.
        In case you are working with C, then this violation
        can be ignored.

    Example::

        # Correct:
        def my_function(first, second):
            ...

        # Wrong:
        def my_function(first, /, second):
            ...

    See also:
        https://www.python.org/dev/peps/pep-0570/

    .. versionadded:: 0.14.0

    """

    error_template = 'Found positional-only argument'
    code = 451


class LoopControlFinallyViolation(ASTViolation):
    """
    Forbid ``break`` and ``continue`` in a ``finally`` block.

    Related to :class:`~TryExceptMultipleReturnPathViolation`.

    Reasoning:
        Putting any control statements in `finally` is a
        terrible practice, because `finally` is implicitly
        called and can cause damage to your logic with
        its implicitness.
        It should not be allowed.

    Solution:
        Remove ``break`` and ``continue`` from ``finally`` blocks.

    Example::

        # Correct:
        try:
            ...
        finally:
            ...

        # Wrong:
        try:
            ...
        finally:
            break

        try:
            ...
        finally:
            continue

    .. versionadded:: 0.14.0

    """

    error_template = 'Found `break` or `continue` in `finally` block'
    code = 452


@final
class ShebangViolation(SimpleViolation):
    """
    Forbid executing a file with shebang incorrectly set.

    A violation is raised in these cases :
        - Shebang is present but the file is not executable.
        - The file is executable but no shebang is present.
        - Shebang is present but does not contain "python".
        - Whitespace is present before the shebang.
        - Presence of blank lines or commented lines before the shebang.

    Reasoning:
        Setting the shebang incorrectly causes an executable mismatch.

    Solution:
        Ensure that the shebang is present on the first line,
        and contains "python", and there is no leading whitespace.

    Example::

        # Correct:
        #!/usr/bin/env python

        # Wrong:
        #!/usr/bin/env
            #!/usr/bin/env python

    .. versionadded:: 0.14.0

    """

    error_template = 'Found executable mismatch: {0}'
    code = 453


@final
class BaseExceptionRaiseViolation(ASTViolation):
    """
    Forbid raising ``Exception`` or ``BaseException``.

    Reasoning:
        ``Exception`` and ``BaseException`` are inconvenient to catch.
        And when you catch them you can accidentally suppress other exceptions.

    Solution:
        Use a user-defined exception, subclassed from ``Exception``.

    Example::

        # Correct:
        raise UserNotFoundError
        raise UserNotFoundError("cannot find user with the given id")

        # Wrong:
        raise Exception
        raise Exception("user not found")
        raise BaseException
        raise BaseException("user not found")

    See also:
        https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

    .. versionadded:: 0.15.0

    """

    error_template = 'Found wrong `raise` exception type: {0}'
    code = 454


@final
class NonTrivialExceptViolation(ASTViolation):
    """
    Forbids using non-trivial expressions as a parameter for ``except``.

    Reasoning:
        Expressions used as an argument for ``except`` could be hard to read
        and hide real list of exceptions being expected
        to occur in the outlined code block.

    Solution:
        Use separate ``except`` blocks for each exception or provide a tuple
        of exception classes.

    Example::

        # Correct:
        try:
            ...
        except ValueError:
            ...
        except TypeError:
            ...

        try:
            ...
        except (TypeError, ValueError):
            ...

        # Wrong:
        try:
            ...
        except TypeError or ValueError:
            ...

    .. versionadded:: 0.15.0

    """

    error_template = 'Found non-trivial expression as an argument for "except"'
    code = 455


@final
class FloatingNanViolation(ASTViolation):
    """
    Forbids using ``float("NaN")`` construct to generate NaN.

    Reasoning:
        This method to generate NaN is really confusing and is a good way to
        catch a lot of unexpected bugs.

    Solution:
        Even if you're 100% sure what you're doing, use ``math.nan`` instead.

    Example::

        # Correct:
        min(math.nan, 3)

        # Wrong:
        min(float("NAN"), 3)

    .. versionadded:: 0.15.0

    """

    error_template = 'Found "NaN" as argument to float()'
    code = 456


@final
class InfiniteWhileLoopViolation(ASTViolation):
    """
    Forbids use of infinite ``while True:`` loops.

    Reasoning:
        Infinite loops will cause bugs in code.

    Solution:
        Add either a return, raise, or break to handle the infinite loop.

    Example::

        # Correct:
        while True:
            print('forever')
            break

        # Wrong:
        while True:
            print('forever')

    .. versionadded:: 0.15.0

    """

    error_template = 'Found an infinite while loop'
    code = 457


@final
class ImportCollisionViolation(ASTViolation):
    """
    Forbids to import from already imported modules.

    Reasoning:
        Importing objects from already imported modules is inconsistent
        and error-prone.

    Solution:
        Do not import objects from already imported modules or use aliases
        when it cannot be avoided.

    Example::

        # Correct:
        import public
        from public.module import FooClass

        import hypothesis
        from hypothesis import strategies as st

        # Wrong:
        from public import utils
        from public.utils import something

        import hypothesis
        from hypothesis import strategies

    .. versionadded:: 0.15.0

    """

    error_template = 'Found imports collision: {0}'
    code = 458


@final
class FloatComplexCompareViolation(ASTViolation):
    """
    Forbids comparisons with ``float`` and ``complex``.

    Reasoning:
        This is a best practice rule, as ``float`` and ``complex``
        suffer from representation error, leading to possibly
        incorrect results during comparison.

    Solution:
        Use fuzzy operators.
        1. ``abs(f1 - f2) <= allowed_error``
        2. ``math.isclose(f1, f2)`` (for ``float``)
        3. ``cmath.isclose(c1, c2)`` (for ``complex``)
        4. Custom logic, not using operators

    Example::

        # Correct:
        math.isclose(3.0, 0.3 / 0.1)
        cmath.isclose(3 + 4j, (0.3 + 0.4j) / 0.1)

        # Wrong:
        3.0 == 0.3 / 0.1
        3 + 4j == (0.3 + 0.4j) / 0.1

    .. versionadded:: 0.15.0

    """

    error_template = 'Found comparison with float or complex number'
    code = 459


@final
class SingleElementDestructuringViolation(ASTViolation):
    """
    Forbids to have single element destructuring.

    Reasoning:
        Having single element destructuring is not readable.

    Solution:
        Use access by index instead.

    Example::

        # Correct:
        first = single_element_list[0]

        # Wrong:
        (first,) = [1]

    .. versionadded:: 0.15.0

    """

    error_template = 'Found single element destructuring'
    code = 460


@final
class ForbiddenInlineIgnoreViolation(SimpleViolation):
    """
    Forbids to use specific inline ignore violations.

    There can be forbidden a specific violation or whole
    class of violations.

    Reasoning:
        There are violations important for specific project that must not
        be ignored, e.g. complexity or best practices violations.

    Solution:
        Remove inline ignore for forbidden violations.

    Configuration:
        This rule is configurable with `--forbidden-inline-ignore``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.FORBIDDEN_INLINE_IGNORE`

    .. versionadded:: 0.15.0

    """

    error_template = 'Forbidden inline ignore: {0}'
    code = 461


@final
class WrongMultilineStringUseViolation(TokenizeViolation):
    '''
    Frobids direct usage of multiline strings.

    Multiline strings are only allowed in docstrings
    or assignments to variables.

    Reasoning:
        Direct usage of multiline strings is not readable.
        One should not depend on the current indentation,
        e.g. in comparisons or function calls.

    Solution:
        Assign a multiline string to a variable.

    Example::

        # Correct:
        multiline = """
            abc
            abc
        """

        # Wrong:
        function("""
            abc
            abc
        """)

    .. versionadded:: 0.15.0

    '''

    error_template = 'Wrong multiline string usage'
    code = 462


@final
class GetterWithoutReturnViolation(ASTViolation):
    """
    Forbids to have functions starting with ``get_`` without returning a value.

    Applies to both methods and functions.

    Reasoning:
        A ``get_`` function is generally expected to return a value. Otherwise,
        it is most likely either an error or bad naming.

    Solution:
        Make sure getter functions ``return`` or ``yield`` a value on all
        execution paths, or rename the function.

    Example::

        # Correct:
        def get_random_number():
             return random.randint(1, 10)

        # Wrong:
        def get_random_number():
             print('I do not return a value!')

    .. versionadded:: 0.15.0

    """

    error_template = 'Found a getter without a return value'
    code = 463


@final
class EmptyCommentViolation(TokenizeViolation):
    """
    Forbid empty comments.

    Empty comments are only allowed in between valid comments.

    Reasoning:
        Empty comments that do not help formatting should be excluded.

    Solution:
        Remove the empty comments.

    Example::

        # Correct:

        # First line
        #
        # Samples:
        # One
        # Two
        my_var = 1

        # Wrong:

        #
        my_var = 1

    .. versionadded:: 0.15.0

    """

    error_template = 'Found empty comment'
    code = 464


@final
class BitwiseAndBooleanMixupViolation(ASTViolation):
    """
    Forbid comparisons between bitwise and boolean expressions.

    Empty comments are only allowed in between valid comments.

    Reasoning:
       This case indicates that a person
       confused ``&`` with ``and`` and ``|`` with ``or``.
       This can be the case if a person is coming from another language.

    Solution:
        Change bitwise operator to boolean operators.

    Example::

        # Correct:
        first | 10

        # Wrong:
        result = ((first > 0) & False)

    .. versionadded:: 0.15.0

    """

    error_template = 'Found likely bitwise and boolean operation mixup'
    code = 465


@final
class NewStyledDecoratorViolation(ASTViolation):
    """
    Forbid using complex grammar for using decorators.

    This violation is only raised for ``python3.9+``,
    earlier versions do not have this concept.

    Reasoning:
       New grammar allows to use decorators in a more liberal way.
       It is probably not a good idea.
       Because decorators should be simple and easy to read.

    Solution:
        Use names, attributes, and calls as decorators only.
        You are free to pass any args to function calls, however.

    Example::

        # Correct:
        @some.decorator(args)
        def my_function(): ...

        # Wrong:
        @some.decorator['method'] + other
        def my_function(): ...

    .. versionadded:: 0.15.0

    """

    error_template = 'Found new-styled decorator'
    code = 466


@final
class BareRaiseViolation(ASTViolation):
    """
    Forbid using a bare ``raise`` keyword outside of ``except``.

    Reasoning:
       Using a bare ``raise`` outside of an ``except`` block
       causes a runtime error.

    Solution:
        Only use bare ``raise`` within an ``except`` block.

    Example::

        # Correct:
        def smth():
            try:
                ...
            except:
                raise

        # Wrong:
        def smth():
            raise

    .. versionadded:: 0.16.0

    """

    error_template = 'Found bare raise keyword'
    code = 467


@final
class RedundantEnumerateViolation(ASTViolation):
    """
    Forbid using a placeholder (``_``) with ``enumerate``.

    Reasoning:
       This adds no value and introduces additional complexity.

    Solution:
        Only use ``enumerate`` when you are going to do something with the
        index it returns.

    Example::

        # Correct:
        for item in items:
          ...

        # Wrong:
        for _, item in enumerate(items):
          ...

    .. versionadded:: 0.16.0

    """

    error_template = 'Found redundant use of `enumerate`'
    code = 468


@final
class RaiseFromItselfViolation(ASTViolation):
    """
    Forbid raising an exception from itself.

    Reasoning:
        It doesn't make sense to raise an exception from it self,
        since the final behavior will be the same.

    Solution:
        Don't raise an exeception from itself.

    Example::

        # Correct:
        ex = Exception('Some Exception')
        raise ex

        # Wrong:
        ex = Exception('Some Exception')
        raise ex from ex

    .. versionadded:: 0.16.0

    """

    error_template = 'Found error raising from itself'
    code = 469


@final
class KwargsUnpackingInClassDefinitionViolation(ASTViolation):
    """
    Forbid kwarg unpacking in class definition.

    Reasoning:
        Dynamic class generation with unknown arguments is bad because it
        creates too much flexibility and possibilities for errors.
        It also limits the typechecking capabilities.

    Solution:
        Use keyword arguments normally without unpacking them.

    Example::

        # Correct:
        class MyClass(argument='argument'):
            ...

        # Wrong:
        arguments = {'argument': 'argument'}
        class MyClass(**arguments):
            ...

    .. versionadded:: 0.16.0

    """

    error_template = 'Found kwarg unpacking in class definition'
    code = 470


@final
class ConsecutiveSlicesViolation(ASTViolation):
    """
    Forbid consecutive slices.

    Reasoning:
        Consecutive slices reduce readability of the code and obscure
        intended meaning of the expression.

    Solution:
        Compress multiple consecutive slices into a single one.

    Example::

        # Correct:
        my_list[1:3]

        # Wrong:
        my_list[1:][:2]

    .. versionadded:: 0.16.0

    """

    error_template = 'Found consecutive slices'
    code = 471


@final
class GettingElementByUnpackingViolation(ASTViolation):
    """
    Forbid getting first element using unpacking.

    Reasoning:
        Performance. Prefixing unused variables with underscore is nothing
        more than convention, Python still creates these variables.
        So, unpacking above makes a new unused list which is slow.

    Solution:
        Use `collection[0]` or `next(iter(collection))`

    Example::

        # Correct:
        first = some_collection[0]
        first = next(iter(collection))

        # Wrong:
        first, *_rest = some_collection

    .. versionadded:: 0.16.0

    """

    error_template = (
        'Found unpacking used to get a single element from a collection'
    )
    code = 472


@final
class WrongEmptyLinesCountViolation(TokenizeViolation):
    """
    Limit empty lines in functions or methods body.

    Reasoning:
        It's not holistic to have functions or methods that contain many
        empty lines, and it makes sense to divide the method into several
        ones.

    Solution:
        Limit count of empty lines of the function or method body
        By default, we allow 1 empty line for 2 non-empty lines.

    Example::

        # Correct:
        def func(name):
            foo()
            if name == 'Moonflower':
                print('Love')
            baz()

        # Wrong:
        def func(name):
            foo()

            if name == 'Moonflower':
                print('Love')

            baz()

    Configuration:
        This rule is configurable with ``--exps-for-one-empty-line``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.EXPS_FOR_ONE_EMPTY_LINE`

    .. versionadded:: 0.17.0

    """

    error_template = 'Found too many empty lines in `def`: {0}'
    code = 473
