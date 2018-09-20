# -*- coding: utf-8 -*-

import ast
from tokenize import TokenInfo
from typing import Generator, Sequence

from flake8.options.manager import OptionManager

from wemake_python_styleguide import constants
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.types import (
    CheckResult,
    ConfigurationOptions,
    TokenVisitorSequence,
    TreeVisitorSequence,
    VisitorSequence,
)
from wemake_python_styleguide.version import version
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ImportMembersVisitor,
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
from wemake_python_styleguide.visitors.ast.general.wrong_function_call import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_import import (
    WrongImportVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    WrongKeywordVisitor,
    WrongRaiseVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_name import (
    WrongModuleMetadataVisitor,
    WrongNameVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_string import (
    WrongStringVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_class import WrongClassVisitor
from wemake_python_styleguide.visitors.ast.wrong_module import (
    WrongContentsVisitor,
)
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)


class Checker(object):
    """
    Main checker class.

    Runs all checks that are bundled with this package.
    If you want to add new checks they should be added to either:

    - ``ast_visitors`` if it is an ``ast`` based visitor
    - ``token_visitors`` if it is a ``token`` based visitor

    """

    name = 'wemake-python-styleguide'
    version = version

    config = Configuration()
    options: ConfigurationOptions

    #: Visitors that should be working by default:
    ast_visitors: TreeVisitorSequence = (
        # General:
        WrongRaiseVisitor,
        WrongFunctionCallVisitor,
        WrongImportVisitor,
        WrongKeywordVisitor,
        WrongNameVisitor,
        WrongModuleMetadataVisitor,
        WrongStringVisitor,
        WrongContentsVisitor,

        # Complexity:
        FunctionComplexityVisitor,
        NestedComplexityVisitor,
        OffsetVisitor,
        ImportMembersVisitor,
        ModuleMembersVisitor,
        MethodMembersVisitor,
        JonesComplexityVisitor,

        # Classes:
        WrongClassVisitor,

        # Modules:
        WrongModuleNameVisitor,
    )

    token_visitors: TokenVisitorSequence = ()

    def __init__(
        self,
        tree: ast.Module,
        file_tokens: Sequence[TokenInfo],
        filename: str = constants.STDIN,
    ) -> None:
        """Creates new checker instance."""
        self.tree = tree
        self.filename = filename
        self.file_tokens = file_tokens

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Calls Configuration instance method for registering options."""
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options: ConfigurationOptions) -> None:
        """Parses registered options for providing to the visitor."""
        cls.options = options

    def _run_checks(
        self,
        visitors: VisitorSequence,
    ) -> Generator[CheckResult, None, None]:
        """Runs all ``ast`` based visitors one by one."""
        for visitor_class in visitors:
            visitor = visitor_class.from_checker(self)
            visitor.run()

            for error in visitor.errors:
                yield (*error.node_items(), type(self))

    def run(self) -> Generator[CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by ``flake8`` API.
        After all configuration is parsed and passed.
        """
        yield from self._run_checks(self.ast_visitors)
        yield from self._run_checks(self.token_visitors)
