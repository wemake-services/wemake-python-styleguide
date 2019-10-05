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

Annotation checks
------------------

.. autoclass:: LiteralNoneViolation

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
