# -*- coding: utf-8 -*-

from ast import Module
from typing import Generator

from flake8.options.manager import OptionManager

from wemake_python_styleguide import constants
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.types import (
    CheckerSequence,
    CheckResult,
    ConfigurationOptions,
)
from wemake_python_styleguide.version import version
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    MethodMembersVisitor,
    ModuleMembersVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.jones import (
    JonesComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NestedComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.offset import (
    OffsetVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_class import WrongClassVisitor
from wemake_python_styleguide.visitors.ast.wrong_contents import (
    WrongContentsVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_function_call import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_import import (
    WrongImportVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_keyword import (
    WrongKeywordVisitor,
    WrongRaiseVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_name import (
    WrongModuleMetadataVisitor,
    WrongNameVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_string import (
    WrongStringVisitor,
)
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)

#: Visitors that should be working by default:
ENABLED_VISITORS: CheckerSequence = [
    # Styling and correctness:
    WrongRaiseVisitor,
    WrongFunctionCallVisitor,
    WrongImportVisitor,
    WrongKeywordVisitor,
    WrongNameVisitor,
    WrongModuleMetadataVisitor,
    WrongClassVisitor,
    WrongStringVisitor,
    WrongContentsVisitor,

    # Complexity:
    FunctionComplexityVisitor,
    NestedComplexityVisitor,
    OffsetVisitor,
    ModuleMembersVisitor,
    MethodMembersVisitor,
    JonesComplexityVisitor,

    # Modules:
    WrongModuleNameVisitor,
]


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

    # Receive `logic_line` as the first argument to make this plugin logical
    def __init__(self, tree: Module, filename: str = constants.STDIN) -> None:
        """Creates new checker instance."""
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Calls Configuration instance method for registering options."""
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options: ConfigurationOptions) -> None:
        """Parses registered options for providing to the visitor."""
        cls.options = options

    def run(self) -> Generator[CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by `flake8` API.
        After all configuration is parsed and passed.
        """
        for visitor_class in ENABLED_VISITORS:
            visitor = visitor_class(
                self.options,
                tree=self.tree,
                filename=self.filename,
            )
            visitor.run()

            for error in visitor.errors:
                yield (*error.node_items(), type(self))
