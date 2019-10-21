# -*- coding: utf-8 -*-

"""
These checks help to prevent incorrect usage of Python 3 typing annotations.

While they maybe of a great help in writing clear
and concise code, they still can be abused.

Once again, these rules are highly subjective. But, we love them.

.. currentmodule:: wemake_python_styleguide.violations.annotations

Summary
-------

.. autosummary::
   :nosignatures:

   LiteralNoneViolation
   NestedAnnotationsViolation
   UnionNestedInOptionalViolation

Annotation checks
------------------

.. autoclass:: LiteralNoneViolation
.. autoclass:: NestedAnnotationsViolation
.. autoclass:: UnionNestedInOptionalViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import ASTViolation


@final
class LiteralNoneViolation(ASTViolation):
    """
    Forbids to use ``Literal[None]`` typing annotation.

    Reasoning:
        Literal[None] is just the same as None.
        There's no need to use the first version.
        It is not type related, it is a consistency rule.

    Solution:
        Replace ``Literal[None]`` with ``None``.

    Example::

        # Correct:
        def func(empty: None):
            '''Empty function.'''

        # Wrong:
        def func(empty: Literal[None]):
            '''Empty function.'''

    .. versionadded:: 0.13.0

    """

    code = 700
    error_template = 'Found useless `Literal[None]` typing annotation'  # noqa: WPS700,E501


@final
class NestedAnnotationsViolation(ASTViolation):
    """
    Forbids use of nested Literal and Union Annotation.

    Reasoning:
        There is no need to nest certain annotations of the same type.
        They are exactly equivalent to the flattened version.
        Use the flattened version for consistency.

    Solution:
        Flatten consecutively nested ``typing.Literal`` and ``typing.Union``.

    Example::

        # Correct:
        Literal[1, 2, 3, "foo", 5, None]
        Union[int, str, float]

        # Wrong:
        Literal[Literal[Literal[1, 2, 3], "foo"], 5, None]
        Union[Union[int, str], float]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found redundant nested typing annotation'
    code = 701


@final
class UnionNestedInOptionalViolation(ASTViolation):
    """
    Forbids to use ``Optional[Union[int, str]]`` annotation.

    Reasoning:
        Optional[Union[int, str]] equals to Union[int, str, None].
        Use Union[int, str, None] version for consistency.

    Solution:
        Replace ``Optional[Union[int, str]]`` with ``Union[int, str, None]``.

    Example::

        # Correct:
        Union[int, str, None]

        # Wrong:
        Optional[Union[int, str]]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found typing annotation with `Union` nested in `Optional`'
    code = 702
