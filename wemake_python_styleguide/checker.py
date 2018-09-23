# -*- coding: utf-8 -*-

import ast
import tokenize
from typing import Generator, Sequence

from flake8.options.manager import OptionManager

from wemake_python_styleguide import constants, types, version
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.visitors.presets import (
    complexity,
    general,
    tokens,
)


class Checker(object):
    """
    Main checker class.

    Runs all checks that are bundled with this package.
    If you want to add new checks they should be added to either:

    - ``ast_visitors`` if it is an ``ast`` based visitor
    - ``token_visitors`` if it is a ``token`` based visitor

    """

    name = version.pkg_name
    version = version.pkg_version

    config = Configuration()
    options: types.ConfigurationOptions

    #: Visitors that should be working by default:
    ast_visitors: types.TreeVisitorSequence = (
        *general.GENERAL_PRESET,
        *complexity.COMPLEXITY_PRESET,
    )

    token_visitors: types.TokenVisitorSequence = (
        *tokens.TOKENS_PRESET,
    )

    def __init__(
        self,
        tree: ast.Module,
        file_tokens: Sequence[tokenize.TokenInfo],
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
    def parse_options(cls, options: types.ConfigurationOptions) -> None:
        """Parses registered options for providing to the visitor."""
        cls.options = options

    def _run_checks(
        self,
        visitors: types.VisitorSequence,
    ) -> Generator[types.CheckResult, None, None]:
        """Runs all ``ast`` based visitors one by one."""
        for visitor_class in visitors:
            visitor = visitor_class.from_checker(self)
            visitor.run()

            for error in visitor.errors:
                yield (*error.node_items(), type(self))

    def run(self) -> Generator[types.CheckResult, None, None]:
        """
        Runs the checker.

        This method is used by ``flake8`` API.
        After all configuration is parsed and passed.
        """
        yield from self._run_checks(self.ast_visitors)
        yield from self._run_checks(self.token_visitors)
