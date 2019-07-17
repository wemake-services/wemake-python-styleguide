# -*- coding: utf-8 -*-

"""
Contains detailed technical information about :term:`violation` internals.

.. _violations:

Violations API
--------------

.. currentmodule:: wemake_python_styleguide.violations.base

.. autoclasstree:: wemake_python_styleguide.violations.base

.. autosummary::
   :nosignatures:

   ASTViolation
   MaybeASTViolation
   TokenizeViolation
   SimpleViolation

Violation can not have more than one base class.
See :ref:`tutorial` for more information about choosing a correct base class.

Conventions
~~~~~~~~~~~

- Each violation class name should end with "Violation"
- Each violation must have a long docstring with full description
- Each violation must have "Reasoning" and "Solution" sections
- Each violation must have "versionadded" policy
- Each violation should have an example with correct and wrong usages
- If violation error template should have a parameter
  it should be the last part of the text: ``: {0}``

Reference
~~~~~~~~~

"""

import ast
import tokenize
from typing import ClassVar, Optional, Set, Tuple, Union

from typing_extensions import final

#: General type for all possible nodes where error happens.
ErrorNode = Union[
    ast.AST,
    tokenize.TokenInfo,
    None,
]


class BaseViolation(object):
    """
    Abstract base class for all style violations.

    It basically just defines how to create any error and how to format
    this error later on.

    Each subclass must define ``error_template`` and ``code`` fields.

    Attributes:
        error_template: message that will be shown to user after formatting.
        code: violation unique number. Used to identify the violation.

    """

    error_template: ClassVar[str]
    code: ClassVar[int]
    previous_codes: ClassVar[Set[int]]

    def __init__(self, node: ErrorNode, text: Optional[str] = None) -> None:
        """
        Creates new instance of abstract violation.

        Parameters:
            node: violation was raised by this node. If applied.
            text: extra text to format the final message. If applied.

        """
        self._node = node
        self._text = text

    @final
    def _full_code(self) -> str:
        """
        Returns fully formatted code.

        Adds violation letter to the numbers.
        Also ensures that codes like ``3`` will be represented as ``WPS003``.
        """
        return 'WPS' + str(self.code).zfill(3)

    def _location(self) -> Tuple[int, int]:
        """
        Return violation location inside the file.

        Default location is in the so-called "file beginning".
        """
        return 0, 0

    @final
    def message(self) -> str:
        """
        Returns error's formatted message with code and reason.

        Conditionally formats the ``error_template`` if it is required.
        """
        return '{0} {1}'.format(
            self._full_code(), self.error_template.format(self._text),
        )

    @final
    def node_items(self) -> Tuple[int, int, str]:
        """Returns tuple to match ``flake8`` API format."""
        return (*self._location(), self.message())


class _BaseASTViolation(BaseViolation):
    """Used as a based type for all ``ast`` violations."""

    _node: Optional[ast.AST]

    @final
    def _location(self) -> Tuple[int, int]:
        line_number = getattr(self._node, 'lineno', 0)
        column_offset = getattr(self._node, 'col_offset', 0)
        return line_number, column_offset


class ASTViolation(_BaseASTViolation):
    """Violation for ``ast`` based style visitors."""

    _node: ast.AST


class MaybeASTViolation(_BaseASTViolation):
    """
    Violation for ``ast`` and modules visitors.

    Is used for violations that share the same rule for nodes and module names.
    Is wildly used for naming rules.
    """

    def __init__(self, node=None, text: Optional[str] = None) -> None:
        """Creates new instance of module violation without explicit node."""
        super().__init__(node, text=text)


class TokenizeViolation(BaseViolation):
    """Violation for ``tokenize`` based visitors."""

    _node: tokenize.TokenInfo

    @final
    def _location(self) -> Tuple[int, int]:
        return self._node.start


class SimpleViolation(BaseViolation):
    """Violation for cases where there's no associated nodes."""

    _node: None

    def __init__(self, node=None, text: Optional[str] = None) -> None:
        """Creates new instance of simple style violation."""
        super().__init__(node, text=text)
