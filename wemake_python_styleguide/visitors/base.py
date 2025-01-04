"""
Contains detailed technical documentation about how to write a :term:`visitor`.

See also:
    Visitor is a well-known software engineering pattern:
    https://en.wikipedia.org/wiki/Visitor_pattern

Each visitor might work with one or many :term:`violations <violation>`.
Multiple visitors might work with the same violation.

.. mermaid::
   :caption: Visitor relation with violations.

    graph TD
        V1[Visitor 1] --> EA[Violation A]
        V1[Visitor 1] --> EB[Violation B]

        V2[Visitor 2] --> EA[Violation A]
        V2[Visitor 2] --> EC[Violation C]

        V3[Visitor 3] --> EZ[Violation WPS]

.. _visitors:

Visitors API
------------

.. currentmodule:: wemake_python_styleguide.visitors.base

.. autoclasstree:: wemake_python_styleguide.visitors.base

.. autosummary::
   :nosignatures:

   BaseNodeVisitor
   BaseFilenameVisitor
   BaseTokenVisitor

The decision relies on what parameters you need for the task.
It is highly unlikely that you will need two parameters at the same time.
See :ref:`tutorial` for more information about choosing a correct base class.

Conventions
~~~~~~~~~~~

Then you will have to write logic for your visitor.
We follow these conventions:

- Public visitor methods start with ``visit_``,
  then comes the name of a token or node to be visited
- All other methods and attributes should be protected
- We try to separate as much logic from ``visit_`` methods as possible,
  so they only route for callbacks that actually execute the checks
- We place repeating logic into ``logic/`` package to be able to reuse it

There are different examples of visitors in this project already.

Reference
~~~~~~~~~

"""

import abc
import ast
import tokenize
from collections.abc import Sequence
from typing import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.routing import route_visit
from wemake_python_styleguide.logic.filenames import get_stem
from wemake_python_styleguide.options.validation import ValidatedOptions
from wemake_python_styleguide.violations.base import BaseViolation


class BaseVisitor(abc.ABC):
    """
    Abstract base class for different types of visitors.

    Attributes:
        options: contains the options objects passed and parsed by ``flake8``.
        filename: filename passed by ``flake8``, each visitor has a file name.
        violations: list of :term:`violations <violation>`
        for the specific visitor.

    """

    def __init__(
        self,
        options: ValidatedOptions,
        filename: str = constants.STDIN,
    ) -> None:
        """Creates base visitor instance."""
        self.options = options
        self.filename = filename
        self.violations: list[BaseViolation] = []

    @classmethod
    def from_checker(
        cls: type['BaseVisitor'],
        checker,
    ) -> 'BaseVisitor':
        """
        Constructs visitor instance from the checker.

        Each unique visitor class should know how to construct itself
        from the :term:`checker` instance.

        Generally speaking, each visitor class needs to eject required
        parameters from checker and then run its constructor
        with these parameters.
        """
        return cls(options=checker.options, filename=checker.filename)

    @final
    def add_violation(self, violation: BaseViolation) -> None:
        """Adds violation to the visitor."""
        # It is not allowed to add disabled violations:
        assert violation.disabled_since is None, violation.code  # noqa: S101
        self.violations.append(violation)

    @abc.abstractmethod
    def run(self) -> None:
        """
        Runs a visitor.

        Each visitor should know what exactly it needs
        to do when it was told to ``run``.
        """

    def _post_visit(self) -> None:  # noqa: B027
        """
        Executed after all nodes have been visited.

        This method is useful for counting statistics, etc.
        By default does nothing.
        """


class BaseNodeVisitor(ast.NodeVisitor, BaseVisitor):
    """
    Allows to store violations while traversing node tree.

    This class should be used as a base class for all ``ast`` based checkers.
    Method ``visit()`` is defined in ``NodeVisitor`` class.

    Attributes:
        tree: ``ast`` tree to be checked.

    """

    def __init__(
        self,
        options: ValidatedOptions,
        tree: ast.AST,
        **kwargs,
    ) -> None:
        """Creates new ``ast`` based instance."""
        super().__init__(options, **kwargs)
        self.tree = tree

    @final
    @classmethod
    def from_checker(
        cls: type['BaseNodeVisitor'],
        checker,
    ) -> 'BaseNodeVisitor':
        """Constructs visitor instance from the checker."""
        return cls(
            options=checker.options,
            filename=checker.filename,
            tree=checker.tree,
        )

    def visit(self, tree: ast.AST) -> None:
        """
        Visits a node.

        Modified version of :class:`ast.NodeVisitor.visit` method.
        We need this to modify how visitors route.

        Why? Because python3.8 now uses ``visit_Constant`` instead of old
        methods like ``visit_Num``, ``visit_Str``, ``visit_Bytes``, etc.

        Some classes do redefine this method to catch all nodes. This is valid.
        """
        return route_visit(self, tree)

    @final
    def run(self) -> None:
        """Recursively visits all ``ast`` nodes. Then executes post hook."""
        self.visit(self.tree)
        self._post_visit()


class BaseFilenameVisitor(BaseVisitor, abc.ABC):
    """
    Abstract base class that allows to visit and check module file names.

    Has ``visit_filename()`` method that should be defined in subclasses.
    """

    stem: str

    @abc.abstractmethod
    def visit_filename(self) -> None:
        """Checks module file names."""

    @final
    def run(self) -> None:
        """
        Checks module's filename.

        Skips modules that are checked as piped output.
        Since these modules are checked as a ``stdin`` input.
        And do not have names.
        """
        if self.filename != constants.STDIN:
            self.stem = get_stem(self.filename)
            self.visit_filename()
            self._post_visit()


class BaseTokenVisitor(BaseVisitor):
    """
    Allows to check ``tokenize`` sequences.

    Attributes:
        file_tokens: ``tokenize.TokenInfo`` sequence to be checked.

    """

    def __init__(
        self,
        options: ValidatedOptions,
        file_tokens: Sequence[tokenize.TokenInfo],
        **kwargs,
    ) -> None:
        """Creates new ``tokenize`` based visitor instance."""
        super().__init__(options, **kwargs)
        self.file_tokens = file_tokens
        self.token_index = -1

    @final
    @classmethod
    def from_checker(
        cls: type['BaseTokenVisitor'],
        checker,
    ) -> 'BaseTokenVisitor':
        """Constructs ``tokenize`` based visitor instance from the checker."""
        return cls(
            options=checker.options,
            filename=checker.filename,
            file_tokens=checker.file_tokens,
        )

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Runs custom defined handlers in a visitor for each specific token type.

        Uses ``.exact_type`` property to fetch the token name.
        So, you have to be extra careful with tokens
        like ``->`` and other operators,
        since they might resolve in just ``OP`` name.

        Does nothing if handler for any token type is not defined.

        Inspired by ``NodeVisitor`` class.

        See also:
            https://docs.python.org/3/library/tokenize.html

        """
        token_type = tokenize.tok_name[token.exact_type].lower()
        method = getattr(self, f'visit_{token_type}', None)
        if method is not None:
            method(token)

    @final
    def run(self) -> None:
        """Visits all token types that have a handler method."""
        for token in self.file_tokens:
            self.visit(token)
        self._post_visit()


class BaseNodeTokenVisitor(ast.NodeVisitor, BaseVisitor):
    """Allows storing violations during node tree traversal with real values."""

    def __init__(
        self,
        options: ValidatedOptions,
        tree: ast.AST,
        file_tokens: Sequence[tokenize.TokenInfo],
        **kwargs,
    ) -> None:
        """Creates new ``ast`` based instance with tokens."""
        super().__init__(options, **kwargs)
        self.tree = tree
        self.file_tokens = file_tokens
        self._token_index = -1
        self._token_dict: dict[tuple[int, int], tokenize.TokenInfo] = {}

    @final
    @classmethod
    def from_checker(
        cls: type['BaseNodeTokenVisitor'], checker
    ) -> 'BaseNodeTokenVisitor':
        """Constructs visitor instance from the checker."""
        return cls(
            options=checker.options,
            filename=checker.filename,
            file_tokens=checker.file_tokens,
            tree=checker.tree,
        )

    def visit(self, tree: ast.AST) -> None:
        """This method does the same as :meth:`BaseNodeVisitor.visit`."""
        return route_visit(self, tree)

    @final
    def run(self) -> None:
        """Recursively visits all ``ast`` nodes and create ``token_dict``."""
        self._create_token_dict()
        self.visit(self.tree)
        self._post_visit()

    def _create_token_dict(self) -> None:
        """Create a token dict."""
        self._token_dict = {token.start: token for token in self.file_tokens}
