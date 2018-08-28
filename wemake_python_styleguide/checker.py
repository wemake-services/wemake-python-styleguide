# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator

from wemake_python_styleguide.compat import maybe_set_parent
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.types import CheckResult, ConfigurationOptions
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

#: Visitors that should be working by default:
ENABLED_VISITORS = (
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


class Checker(object):
    """
    Main checker class.

    Runs all checks that are bundled with this package.
    If you want to add new checks they should be added to ``ENABLED_VISITORS``.
    """

    name = 'wemake-python-styleguide'
    version = version

    config = Configuration()
    options: ConfigurationOptions

    def __init__(self, tree: Module, filename: str = '-') -> None:
        """Creates new checker instance."""
        self.tree = maybe_set_parent(tree)
        self.filename = filename

    @classmethod
    def add_options(cls, parser):  # TODO: types
        """Calls Configuration instance method for registering options."""
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options: ConfigurationOptions):
        """Parses registered options for providing to the visiter."""
        cls.options = options

    def run(self) -> Generator[CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by `flake8` API.
        After all configuration is parsed and passed.
        """
        for visitor_class in ENABLED_VISITORS:
            visiter = visitor_class()
            visiter.provide_options(self.options)
            visiter.visit(self.tree)

            for error in visiter.errors:
                yield (*error.node_items(), type(self))
