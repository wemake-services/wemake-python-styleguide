# -*- coding: utf-8 -*-

import ast
import tokenize
from typing import List, Sequence, Type

from wemake_python_styleguide import constants
from wemake_python_styleguide.errors.base import BaseStyleViolation
from wemake_python_styleguide.types import ConfigurationOptions


class BaseVisitor(object):
    """
    Base class for different types of visitors.

    Attributes:
        options: contains the options objects passed and parsed by ``flake8``.
        filename: filename passed by ``flake8``.
        errors: list of errors for the specific visitor.

    """

    def __init__(
        self,
        options: ConfigurationOptions,
        filename: str = constants.STDIN,
    ) -> None:
        """Create base visitor instance."""
        self.options = options
        self.filename = filename
        self.errors: List[BaseStyleViolation] = []

    @classmethod
    def from_checker(cls: Type['BaseVisitor'], checker) -> 'BaseVisitor':
        """Constructs visitor instance from the checker."""
        return cls(options=checker.options, filename=checker.filename)

    def add_error(self, error: BaseStyleViolation) -> None:
        """Adds error to the visitor."""
        self.errors.append(error)

    def run(self) -> None:
        """This method should be defined in all subclasses of this class."""
        raise NotImplementedError('Should be defined in a subclass')


class BaseNodeVisitor(ast.NodeVisitor, BaseVisitor):
    """
    Allows to store errors while traversing node tree.

    This class should be used as a base class for all ``ast`` based checkers.
    Method ``visit()`` is defined in ``NodeVisitor`` class.

    Attributes:
        tree: ``ast`` tree to be checked.

    """

    def __init__(
        self,
        options: ConfigurationOptions,
        tree: ast.AST,
        **kwargs,
    ) -> None:
        """Creates new ``ast`` based instance."""
        super().__init__(options, **kwargs)
        self.tree = tree

    @classmethod
    def from_checker(
        cls: Type['BaseNodeVisitor'],
        checker,
    ) -> 'BaseNodeVisitor':
        """Constructs visitor instance from the checker."""
        return cls(
            options=checker.options,
            filename=checker.filename,
            tree=checker.tree,
        )

    def _post_visit(self) -> None:
        """
        Executed after all nodes have been visited.

        By default does nothing.
        """

    def run(self) -> None:
        """Recursively visits all ``ast`` nodes. Then executes post hook."""
        self.visit(self.tree)
        self._post_visit()


class BaseFilenameVisitor(BaseVisitor):
    """
    Allows to check module file names.

    Has ``visit_filename()`` method that should be redefined in subclasses.
    """

    def visit_filename(self) -> None:
        """This method should be overridden in a subclass."""
        raise NotImplementedError('Should be defined in a subclass')

    def run(self) -> None:
        """Checks module's filename."""
        if self.filename != constants.STDIN:
            self.visit_filename()


class BaseTokenVisitor(BaseVisitor):
    """Allows to check ``tokenize`` sequences."""

    def __init__(
        self,
        options: ConfigurationOptions,
        file_tokens: Sequence[tokenize.TokenInfo],
        **kwargs,
    ) -> None:
        """Creates new ``tokenize`` based instance."""
        super().__init__(options, **kwargs)
        self.file_tokens = file_tokens

    @classmethod
    def from_checker(
        cls: Type['BaseTokenVisitor'],
        checker,
    ) -> 'BaseTokenVisitor':
        """Constructs visitor instance from the checker."""
        return cls(
            options=checker.options,
            filename=checker.filename,
            file_tokens=checker.file_tokens,
        )

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Runs custom defined handlers for each specific token type."""
        token_type = tokenize.tok_name[token.exact_type].lower()
        method = getattr(self, 'visit_' + token_type, None)
        if method is not None:
            method(token)

    def run(self) -> None:
        """Visits all token types."""
        for token in self.file_tokens:
            self.visit(token)
