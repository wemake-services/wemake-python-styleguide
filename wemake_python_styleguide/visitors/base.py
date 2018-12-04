# -*- coding: utf-8 -*-

"""
Contains detailed documentation about how to write a visitor.

.. _visitors:

Creating new visitor
--------------------

First of all, you have to decide what base class do you want to use?

.. currentmodule:: wemake_python_styleguide.visitors.base

Available base classes
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   BaseNodeVisitor
   BaseFilenameVisitor
   BaseTokenVisitor

The decision relies on what parameters do you need for the task.
It is highly unlikely that you will need two parameters at the same time.

Visitors API
------------

"""

import ast
import tokenize
from typing import List, Sequence, Type

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics.filenames import get_stem
from wemake_python_styleguide.types import ConfigurationOptions, final
from wemake_python_styleguide.violations.base import BaseViolation


class BaseVisitor(object):
    """
    Abstract base class for different types of visitors.

    Attributes:
        options: contains the options objects passed and parsed by ``flake8``.
        filename: filename passed by ``flake8``, each visitor has a file name.
        violations: list of violations for the specific visitor.

    """

    def __init__(
        self,
        options: ConfigurationOptions,
        filename: str = constants.STDIN,
    ) -> None:
        """Creates base visitor instance."""
        self.options = options
        self.filename = filename
        self.violations: List[BaseViolation] = []

    @classmethod
    def from_checker(cls: Type['BaseVisitor'], checker) -> 'BaseVisitor':
        """
        Constructs visitor instance from the checker.

        Each unique visitor class should know how to construct itself
        from the ``checker`` instance.

        Generally speaking, each visitor class needs to eject required
        parameters from checker and then run
        its constructor with these parameters.
        """
        return cls(options=checker.options, filename=checker.filename)

    @final
    def add_violation(self, violation: BaseViolation) -> None:
        """Adds violation to the visitor."""
        self.violations.append(violation)

    def run(self) -> None:
        """
        Abstract method to run a visitor.

        Each visitor should know what exactly it needs
        to do when it was told to ``run``.
        This method should be defined in all subclasses.
        """
        raise NotImplementedError('Should be defined in a subclass')

    def _post_visit(self) -> None:
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
        options: ConfigurationOptions,
        tree: ast.AST,
        **kwargs,
    ) -> None:
        """Creates new ``ast`` based instance."""
        super().__init__(options, **kwargs)
        self.tree = tree

    @final
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

    @final
    def run(self) -> None:
        """Recursively visits all ``ast`` nodes. Then executes post hook."""
        self.visit(self.tree)
        self._post_visit()


class BaseFilenameVisitor(BaseVisitor):
    """
    Abstract base class that allows to visit and check module file names.

    Has ``visit_filename()`` method that should be defined in subclasses.
    """

    stem: str

    def visit_filename(self) -> None:
        """
        Abstract method to check module file names.

        This method should be overridden in a subclass.
        """
        raise NotImplementedError('Should be defined in a subclass')

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
        options: ConfigurationOptions,
        file_tokens: Sequence[tokenize.TokenInfo],
        **kwargs,
    ) -> None:
        """Creates new ``tokenize`` based visitor instance."""
        super().__init__(options, **kwargs)
        self.file_tokens = file_tokens

    @final
    @classmethod
    def from_checker(
        cls: Type['BaseTokenVisitor'],
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

        See also:
            https://docs.python.org/3/library/tokenize.html

        """
        token_type = tokenize.tok_name[token.exact_type].lower()
        method = getattr(self, 'visit_' + token_type, None)
        if method is not None:
            method(token)

    @final
    def run(self) -> None:
        """Visits all token types that have a handler method."""
        for token in self.file_tokens:
            self.visit(token)
        self._post_visit()
