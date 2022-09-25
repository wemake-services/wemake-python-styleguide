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

Violation cannot have more than one base class.
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

Deprecating a violation
~~~~~~~~~~~~~~~~~~~~~~~

When you want to mark some violation as deprecated,
then assign ``deprecated`` boolean flag to it:

.. code:: python

  @final
  class SomeViolation(ASTViolation):
      deprecated = True

Reference
~~~~~~~~~

"""

import abc
import ast
import enum
import tokenize
from typing import Callable, ClassVar, Optional, Set, Tuple, Union

from typing_extensions import TypeAlias, final

#: General type for all possible nodes where error happens.
ErrorNode: TypeAlias = Union[
    ast.AST,
    tokenize.TokenInfo,
    None,
]

#: We use this type to define helper classes with callbacks to add violations.
ErrorCallback: TypeAlias = Callable[['BaseViolation'], None]


@enum.unique
class ViolationPostfixes(enum.Enum):
    """String values of postfixes used for violation baselines."""

    bigger_than = ' > {0}'
    less_than = ' < {0}'


# TODO: remove `noqa` after a new release (0.17.0):
class BaseViolation(object, metaclass=abc.ABCMeta):  # noqa: WPS338
    """
    Abstract base class for all style violations.

    It basically just defines how to create any error and how to format
    this error later on.

    Each subclass must define ``error_template`` and ``code`` fields.

    Attributes:
        error_template: message that will be shown to user after formatting.
        code: unique violation number. Used to identify the violation.
        previous_codes: just a documentation thing to track changes in time.
        deprecated: indicates that this violation will be removed soon.
        postfix_template: indicates message that we show at the very end.

    """

    error_template: ClassVar[str]
    code: ClassVar[int]
    previous_codes: ClassVar[Set[int]]
    deprecated: ClassVar[bool] = False

    # assigned in __init_subclass__
    full_code: ClassVar[str]
    summary: ClassVar[str]

    # We use this code to show base metrics and thresholds mostly:
    postfix_template: ClassVar[ViolationPostfixes] = (
        ViolationPostfixes.bigger_than
    )

    def __init_subclass__(cls, **kwargs) -> None:
        """Sets additional values for subclasses."""
        super().__init_subclass__(**kwargs)
        violation_code = getattr(cls, 'code', None)
        if violation_code is None:
            return
        if cls.__doc__ is None:
            raise TypeError(
                'Please include a docstring documenting {0}'.format(cls),
            )
        # this is mostly done for docs to display the full code,
        # allowing its indexing in search engines and better discoverability
        cls.full_code = cls._full_code()
        cls.summary = cls.__doc__.lstrip().split('\n', maxsplit=1)[0]
        # this hack adds full code to summary table in the docs
        cls.__doc__ = _prepend_skipping_whitespaces(
            '{0} — '.format(cls.full_code), cls.__doc__,
        )

    def __init__(
        self,
        node: ErrorNode,
        text: Optional[str] = None,
        baseline: Optional[int] = None,
    ) -> None:
        """
        Creates a new instance of an abstract violation.

        Arguments:
            node: violation was raised by this node. If applicable.
            text: extra text to format the final message. If applicable.
            baseline: some complexity violations show the logic threshold here.

        """
        self._node = node
        self._text = text
        self._baseline = baseline

    @final
    def message(self) -> str:
        """
        Returns error's formatted message with code and reason.

        Conditionally formats the ``error_template`` if it is required.
        """
        return '{0} {1}{2}'.format(
            self.full_code,
            self.error_template.format(self._text),
            self._postfix_information(),
        )

    @final
    def node_items(self) -> Tuple[int, int, str]:
        """Returns tuple to match ``flake8`` API format."""
        return (*self._location(), self.message())

    @final
    @classmethod
    def _full_code(cls) -> str:
        """
        Returns fully formatted code.

        Adds violation letter to the numbers.
        Also ensures that codes like ``3`` will be represented as ``WPS003``.
        """
        return 'WPS{0}'.format(str(cls.code).zfill(3))

    @final
    def _postfix_information(self) -> str:
        """
        Adds useful information to the end of the violation message.

        Useful for complexity baselines and other thresholds.
        """
        if self._baseline is None:
            return ''
        return self.postfix_template.value.format(self._baseline)

    @abc.abstractmethod
    def _location(self) -> Tuple[int, int]:
        """Base method for showing error location."""


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

    def __init__(
        self,
        node: Optional[ast.AST] = None,
        text: Optional[str] = None,
        baseline: Optional[int] = None,
    ) -> None:
        """Creates new instance of module violation without explicit node."""
        super().__init__(node, text=text, baseline=baseline)


class TokenizeViolation(BaseViolation):
    """Violation for ``tokenize`` based visitors."""

    _node: tokenize.TokenInfo

    @final
    def _location(self) -> Tuple[int, int]:
        return self._node.start


class SimpleViolation(BaseViolation):
    """Violation for cases where there's no associated nodes."""

    _node: None

    def __init__(
        self,
        node=None,
        text: Optional[str] = None,
        baseline: Optional[int] = None,
    ) -> None:
        """Creates new instance of simple style violation."""
        super().__init__(node, text=text, baseline=baseline)

    @final
    def _location(self) -> Tuple[int, int]:
        """
        Return violation location inside the file.

        Default location is in the so-called "file beginning".
        Cannot be ignored by inline ``noqa`` comments.
        """
        return 0, 0


def _prepend_skipping_whitespaces(prefix: str, text: str) -> str:
    lstripped_text = text.lstrip()
    leading_whitespaces = text[:len(text) - len(lstripped_text)]
    return leading_whitespaces + prefix + lstripped_text
