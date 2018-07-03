# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator, Tuple

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
from wemake_python_styleguide.visitors.wrong_name import (
    WrongModuleMetadataVisitor,
    WrongNameVisitor,
)
from wemake_python_styleguide.visitors.wrong_nested import WrongNestedVisitor

CheckResult = Tuple[int, int, str, type]


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
            WrongNameVisitor,
            WrongModuleMetadataVisitor,
        )

    def run(self) -> Generator[CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by `flake8` API.
        """
        for visitor_class in self._visitors:
            visiter = visitor_class()
            visiter.visit(self.tree)

            for error in visiter.errors:
                lineno, col_offset, message = error.node_items()
                yield lineno, col_offset, message, type(self)
