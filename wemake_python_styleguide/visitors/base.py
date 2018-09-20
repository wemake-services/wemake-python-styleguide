# -*- coding: utf-8 -*-

import ast
from typing import List, Type

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
        """Runs the checking process."""
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
