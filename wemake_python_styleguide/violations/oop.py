"""
These checks ensures that you use Python's version of OOP correctly.

There are different gotchas in Python to write beatiful classes
and using objects correctly. That's the place we collect these kind of rules.

.. currentmodule:: wemake_python_styleguide.violations.oop

Summary
-------

.. autosummary::
   :nosignatures:

   BuiltinSubclassViolation
   ShadowedClassAttributeViolation
   StaticMethodViolation
   BadMagicMethodViolation
   WrongClassBodyContentViolation
   MethodWithoutArgumentsViolation
   WrongBaseClassViolation
   WrongSlotsViolation
   WrongSuperCallViolation
   DirectMagicAttributeAccessViolation
   AsyncMagicMethodViolation
   YieldMagicMethodViolation
   UselessOverwrittenMethodViolation
   WrongSuperCallAccessViolation

Respect your objects
--------------------

.. autoclass:: BuiltinSubclassViolation
.. autoclass:: ShadowedClassAttributeViolation
.. autoclass:: StaticMethodViolation
.. autoclass:: BadMagicMethodViolation
.. autoclass:: WrongClassBodyContentViolation
.. autoclass:: MethodWithoutArgumentsViolation
.. autoclass:: WrongBaseClassViolation
.. autoclass:: WrongSlotsViolation
.. autoclass:: WrongSuperCallViolation
.. autoclass:: DirectMagicAttributeAccessViolation
.. autoclass:: AsyncMagicMethodViolation
.. autoclass:: YieldMagicMethodViolation
.. autoclass:: UselessOverwrittenMethodViolation
.. autoclass:: WrongSuperCallAccessViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import ASTViolation


@final
class BuiltinSubclassViolation(ASTViolation):
    """
    Forbids to subclass lowercase builtins.

    We forbid to subclass builtins like ``int``, ``str``, ``bool``, etc.
    We allow to subclass ``object`` and ``type``, warnings, and exceptions.

    See
    :py:data:`~wemake_python_styleguide.constants.ALLOWED_BUILTIN_CLASSES`
    for the whole list of whitelisted names.

    Reasoning:
        It is almost never a good idea (unless you do something sneaky)
        to subclass primitive builtins.

    Solution:
        Use custom objects around some wrapper.
        Use magic methods to emulate the desired behaviour.

    Example::

        # Correct:
        class Some(object): ...
        class MyValueException(ValueError): ...

        # Wrong:
        class MyInt(int): ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found subclassing a builtin: {0}'
    code = 600
    previous_codes = {426}


@final
class ShadowedClassAttributeViolation(ASTViolation):
    """
    Forbids to shadow class level attributes with instance level attributes.

    Reasoning:
        This way you will have two attributes inside your ``__mro__`` chain:
        one from instance and one from class. It might cause errors.
        Needless to say, that this is just pointless to do so.

    Solution:
        Use either class attributes or instance attributes.
        Use ``ClassVar`` type on fields that are declared as class attributes.

    Note, that we cannot find shadowed attributes that are defined
    in parent classes. That's where ``ClassVar`` is required for ``mypy``
    to check it for you.

    Example::

        # Correct:
        from typing import ClassVar

        class First(object):
            field: ClassVar[int] = 1

        class Second(object):
            field: int

            def __init__(self) -> None:
                self.field = 1

        # Wrong:
        class Some(object):
            field = 1

            def __init__(self) -> None:
                self.field = 1

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found shadowed class attribute: {0}'
    code = 601
    previous_codes = {427}


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
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found using `@staticmethod`'
    code = 602
    previous_codes = {433}


@final
class BadMagicMethodViolation(ASTViolation):
    """
    Forbids to use some magic methods.

    Reasoning:
        We forbid to use magic methods related to the forbidden language parts.
        Likewise, we forbid to use ``del`` keyword, so we forbid to use all
        magic methods related to it.

    Solution:
        Refactor your code to use custom methods instead.
        It will give more context to your app.

    See
    :py:data:`~wemake_python_styleguide.constants.MAGIC_METHODS_BLACKLIST`
    for the full blacklist of the magic methods.

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.11.0

    See also:
        https://www.youtube.com/watch?v=F6u5rhUQ6dU

    """

    error_template = 'Found using restricted magic method: {0}'
    code = 603
    previous_codes = {434}


@final
class WrongClassBodyContentViolation(ASTViolation):
    """
    Forbids to use incorrect nodes inside ``class`` definitions.

    Reasoning:
        Python allows us to have conditions, context managers,
        and even infinite loops inside ``class`` definitions.
        On the other hand, only methods, attributes, and docstrings make sense.
        So, we discourage using anything except these nodes in class bodies.

    Solution:
        If you have complex logic inside your class definition,
        most likely that you do something wrong.
        There are different options to refactor this mess.
        You can try metaclasses, decorators, builders, and other patterns.

    Example::

        # Wrong:
        class Test(object):
            for _ in range(10):
                print('What?!')

    We also allow some nested classes,
    check out :class:`NestedClassViolation` for more information.

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found incorrect node inside `class` body'
    code = 604
    previous_codes = {452}


@final
class MethodWithoutArgumentsViolation(ASTViolation):
    """
    Forbids to have methods without any arguments.

    Reasoning:
        Methods without arguments are allowed to be defined,
        but almost impossible to use.
        Furthermore, they don't have an access to ``self``,
        so cannot access the inner state of the object.
        It might be an intentional design or just a typo.

    Solution:
        Move any methods with arguments to raw functions.
        Or just add an argument if it is actually required.

    Example::

        # Correct:
        class Test(object):
            def method(self): ...

        # Wrong:
        class Test(object):
            def method(): ...

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found method without arguments: {0}'
    code = 605
    previous_codes = {453}


@final
class WrongBaseClassViolation(ASTViolation):
    """
    Forbids to have anything else than a class as a base class.

    We only check base classes and not keywords. They can be anything you need.

    Reasoning:
        In Python you can specify anything in the base classes slot.
        In runtime this expression will be evaluated and executed.
        We need to prevent dirty hacks in this field.

    Solution:
        Use only attributes, names, and types to be your base classes.
        Use ``annotation`` future import in case
        you use strings in base classes.

    Example::

        # Correct:
        class Test(module.ObjectName, MixinName, keyword=True): ...
        class GenericClass(Generic[ValueType]): ...

        # Wrong:
        class Test((lambda: object)()): ...

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.7.1
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.12.0

    """

    error_template = 'Found incorrect base class'
    code = 606
    previous_codes = {454}


@final
class WrongSlotsViolation(ASTViolation):
    """
    Forbids to have incorrect ``__slots__`` definition.

    Things that this rule checks:

    - That ``__slots__`` is a tuple, name, attribute, star, or call
    - That ``__slots__`` do not have duplicates
    - That ``__slots__`` do not have empty strings or invalid python names

    Reasoning:
        ``__slots__`` is a very special attribute.
        It completely changes your class. So, we need to be careful with it.
        We should not allow anything rather than tuples to define slots,
        we also need to check that fields defined in ``__slots__`` are unique.

    Solution:
        Use tuples with unique elements to define ``__slots__`` attribute.
        Use ``snake_case`` to define attributes in ``__slots__``.

    Example::

        # Correct:
        class Test(object):
            __slots__ = ('field1', 'field2')

        class Other(Test):
            __slots__ = (*Test.__slots__, 'child')

        # Wrong:
        class Test(object):
            __slots__ = ['field1', 'field2', 'field2']

    Note, that we do ignore all complex expressions for this field.
    So, we only check raw literals.

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.12.0

    """

    error_template = 'Found incorrect `__slots__` syntax'
    code = 607
    previous_codes = {455}


@final
class WrongSuperCallViolation(ASTViolation):
    """
    Forbids to use ``super()`` with parameters or outside of methods.

    Reasoning:
        ``super()`` is a very special function.
        It implicitly relies on the context where it is used
        and parameters passed to it.
        So, we should be very careful with parameters and context.

    Solution:
        Use ``super()`` without arguments and only inside methods.

    Example::

        # Correct:
        super().__init__()

        # Wrong:
        super(ClassName, self).__init__()

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found incorrect `super()` call: {0}'
    code = 608
    previous_codes = {456}


@final
class DirectMagicAttributeAccessViolation(ASTViolation):
    """
    Forbids to use direct magic attributes and methods.

    Reasoning:
        When using direct magic attributes or method
        it means that you are doing something wrong.
        Magic methods are not suited to be directly called or accessed.

    Solution:
        Use special syntax constructs that will call underlying magic methods.

    Example::

        # Correct:
        super().__init__()

        # Wrong:
        2..__truediv__(2)
        d.__delitem__('a')

    Note, that it is possible to use direct magic attributes with
    ``self``, ``cls``, and ``super()`` as base names.
    We allow this because a lot of internal logic relies on these methods.

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found direct magic attribute usage: {0}'
    code = 609
    previous_codes = {462}


@final
class AsyncMagicMethodViolation(ASTViolation):
    """
    Forbids to make some magic methods async.

    We allow to make ``__anext__``, ``__aenter__``, ``__aexit__`` async.
    We also allow custom magic methods to be async.

    See
    :py:data:`~wemake_python_styleguide.constants.ASYNC_MAGIC_METHODS_BLACKLIST`
    for the whole list of blacklisted async magic methods.

    Reasoning:
        Defining the magic methods as async which are not supposed
        to be async would not work as expected.

    Solution:
        Do not make this magic method async.

    Example::

        # Correct:
        class Test(object):
            def __lt__(self, other): ...

        # Wrong:
        class Test(object):
            async def __lt__(self, other): ...

    See also:
        https://docs.python.org/3/reference/datamodel.html

    .. versionadded:: 0.12.0

    """

    error_template = 'Found forbidden `async` magic method usage: {0}'
    code = 610


@final
class YieldMagicMethodViolation(ASTViolation):
    """
    Forbids to use ``yield`` inside of several magic methods.

    We allow to make ``__iter__`` a generator.
    See
    :py:data:`~wemake_python_styleguide.constants.YIELD_MAGIC_METHODS_BLACKLIST`
    for the whole list of blacklisted generator magic methods.

    Reasoning:
        Python's datamodel is strict.
        You cannot make generators from random magic methods.
        This rule enforces it.

    Solution:
        Remove ``yield`` from a magic method
        or rename it to be a custom method.

    Example::

         # Correct:
        class Example(object):
            def __init__(self):
                ...

        # Wrong:
        class Example(object):
            def __init__(self):
                yield 10

    See also:
        https://docs.python.org/3/reference/datamodel.html

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.11.0
    .. versionchanged:: 0.12.0

    """

    error_template = 'Found forbidden `yield` magic method usage'
    code = 611
    previous_codes = {439, 435}


@final
class UselessOverwrittenMethodViolation(ASTViolation):
    """
    Forbids to have useless overwritten methods.

    Reasoning:
        Overwriting method without any changes
        does not have any positive impact.

    Solution:
        Do not overwrite method in case you do not want
        to do any changes inside it.

    Example::

        # Correct:
        class Test(Base):
            def method(self, argument):
                super().method(argument)
                return argument  # or None, or anything!

        # Wrong:
        class Test(object):
            def method(self, argument):
                return super().method(argument)


    .. versionadded:: 0.12.0

    """

    error_template = 'Found useless overwritten method: {0}'
    code = 612


@final
class WrongSuperCallAccessViolation(ASTViolation):
    """
    Forbids to use ``super()`` with incorrect methods or properties access.

    Reasoning:
        Can only use ``super()`` method that matches the following context.
        ``super().some()`` and ``super().some`` in ``Child.some()``,
        and ``super().prop`` and ``super().prop()`` in ``Child.prop``

    Solution:
        Use ``super()`` methods and properties with the correct context.

    Example::

        # Correct:
        class Child(Parent):
            def some_method(self):
                original = super().some_method()

        # Wrong:
        class Child(Parent):
            def some_method(self):
                other = super().other_method()


    .. versionadded:: 0.13.0

    """

    error_template = (
        'Found incorrect `super()` call context: incorrect name access'
    )
    code = 613
