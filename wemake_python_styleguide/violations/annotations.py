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

Annotation checks
------------------

.. autoclass:: LiteralNoneViolation
.. autoclass:: NestedAnnotationsViolation

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

    code = 701
    error_template = 'Found useless `Literal[None]` typing annotation'


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
    code = 702
