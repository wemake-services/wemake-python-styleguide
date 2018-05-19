# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator

from wemake_python_styleguide.version import __version__
from wemake_python_styleguide.visitors.high_complexity import ComplexityVisitor
from wemake_python_styleguide.visitors.wrong_function_call import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.wrong_import import WrongImportVisitor
from wemake_python_styleguide.visitors.wrong_keyword import (
    WrongKeywordVisitor,
    WrongRaiseVisitor,
)
from wemake_python_styleguide.visitors.wrong_nested import WrongNestedVisitor
from wemake_python_styleguide.visitors.wrong_variable import (
    WrongModuleMetadata,
    WrongVariableVisitor,
)


class Checker(object):
    """
    Main checker class.

    Runs all possible checks.
    """

    name = 'wemake-python-styleguide'
    version = __version__

    def __init__(self, tree: Module, filename: str = '-') -> None:
        """Creates new checker instance."""
        self.tree = tree
        self.filename = filename

        self._visitors = (
            WrongRaiseVisitor,
            WrongFunctionCallVisitor,
            WrongImportVisitor,
            WrongKeywordVisitor,
            WrongNestedVisitor,
            ComplexityVisitor,
            WrongVariableVisitor,
            WrongModuleMetadata,
        )

    def run(self) -> Generator[tuple, None, None]:
        """
        Runs the checker.

        This method is used by `flake8` API.
        """
        for visitor_class in self._visitors:
            visiter = visitor_class()
            visiter.visit(self.tree)

            for error in visiter.errors:
                lineno, col_offset, message = error.items()
                yield lineno, col_offset, message, type(self)
