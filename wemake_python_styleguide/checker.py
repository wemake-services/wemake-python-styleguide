# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator, Tuple

from wemake_python_styleguide.compat import maybe_set_parent
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.version import version
from wemake_python_styleguide.visitors.high_complexity import ComplexityVisitor
from wemake_python_styleguide.visitors.wrong_class import WrongClassVisitor
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
    version = version

    config = Configuration()
    options = None  # So that mypy could detect the attribute

    def __init__(self, tree: Module, filename: str = '-') -> None:
        """Creates new checker instance."""
        self.tree = maybe_set_parent(tree)
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
            WrongClassVisitor,
        )

    @classmethod
    def add_options(cls, parser):
        """Calls Configuration instance method for registering options."""
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options):
        """Parses registered options for providing to the visiter."""
        cls.options = options

    def run(self) -> Generator[CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by `flake8` API.
        """
        for visitor_class in self._visitors:
            visiter = visitor_class()
            visiter.provide_options(self.options)
            visiter.visit(self.tree)

            for error in visiter.errors:
                lineno, col_offset, message = error.node_items()
                yield lineno, col_offset, message, type(self)
