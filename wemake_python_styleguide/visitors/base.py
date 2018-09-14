# -*- coding: utf-8 -*-

import ast
from typing import List

from wemake_python_styleguide import constants
from wemake_python_styleguide.errors.base import BaseStyleViolation
from wemake_python_styleguide.types import ConfigurationOptions


class BaseChecker(object):
    """
    Base class for different type of checkers.

    Attributes:
        tree: AST tree to be checked if any.
        options: contains the options objects passed and parsed by ``flake8``.
        filename: filename passed by ``flake8``.
        errors: list of errors for the specific checker.

    """

    def __init__(
        self,
        options: ConfigurationOptions,
        tree: ast.AST = None,
        filename: str = 'stdin',
    ) -> None:
        """Creates new  instance."""
        super().__init__()
        self.options = options
        self.tree = tree
        self.filename = filename
        self.errors: List[BaseStyleViolation] = []

    def add_error(self, error: BaseStyleViolation) -> None:
        """Adds error to the visitor."""
        self.errors.append(error)

    def run(self) -> None:
        """This method should be defined in all subclasses of this class."""
        raise NotImplementedError('Should be defined in a subclass')


class BaseNodeVisitor(ast.NodeVisitor, BaseChecker):
    """
    This class allows to store errors while traversing node tree.

    This class should be used as a base class for all ``ast``- based checkers.
    Method ``visit()`` is defined in ``NodeVisitor`` class.
    """

    def _post_visit(self) -> None:
        """
        This method is executed after all nodes have been visited.

        By default, does nothing.
        """

    def run(self) -> None:
        """Runs the checking process."""
        if self.tree is None:
            raise ValueError('Parsing without a defined tree')
        self.visit(self.tree)
        self._post_visit()


class BaseFilenameVisitor(BaseChecker):
    """
    This class allows to check module filenames.

    Method `visit()` is used only for API compatibility.
    """

    def visit_filename(self) -> None:
        """This method should be overridden in a subclass."""
        raise NotImplementedError('Should be defined in a subclass')

    def run(self) -> None:
        """
        Checks module's filename.

        If filename equals to ``STDIN`` constant then this check is ignored.
        Otherwise, runs ``visit_filename()`` method.
        """
        if self.filename != constants.STDIN:
            self.visit_filename()
