# -*- coding: utf-8 -*-

"""
Entry point to the app.

Represents a :term:`checker` business entity.
There's only a single checker instance
that runs a lot of :term:`visitors <visitor>`.

.. mermaid::
   :caption: Checker relation with visitors.

    graph TD
        C1[Checker] --> V1[Visitor 1]
        C1[Checker] --> V2[Visitor 2]
        C1[Checker] --> VN[Visitor N]

That's how all ``flake8`` plugins work:

.. mermaid::
   :caption: ``flake8`` API calls order.

    graph LR
        F1[flake8] --> F2[add_options]
        F2         --> F3[parse_options]
        F3         --> F4[__init__]
        F4	       --> F5[run]

.. _checker:

Checker API
-----------

.. autoclass:: Checker
   :no-undoc-members:
   :exclude-members: name, version, visitors, _run_checks
   :special-members: __init__

"""

import ast
import tokenize
from typing import ClassVar, Iterator, Sequence, Type

from flake8.options.manager import OptionManager
from typing_extensions import final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide import version as pkg_version
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.options.validation import validate_options
from wemake_python_styleguide.presets import complexity, general, tokens
from wemake_python_styleguide.transformations.ast_tree import transform
from wemake_python_styleguide.visitors import base

VisitorClass = Type[base.BaseVisitor]


@final
class Checker(object):
    """
    Implementation of :term:`checker`.

    See also:
        http://flake8.pycqa.org/en/latest/plugin-development/index.html

    Attributes:
        name: required by the ``flake8`` API, should match the package name.
        version: required by the ``flake8`` API, defined in the packaging file.
        config: custom configuration object used to provide and parse options:
        :class:`wemake_python_styleguide.options.config.Configuration`.

        options: option structure passed by ``flake8``:
        :class:`wemake_python_styleguide.types.ConfigurationOptions`.

        visitors: :term:`preset` of visitors that are run by this checker.

    """

    name: ClassVar[str] = pkg_version.pkg_name
    version: ClassVar[str] = pkg_version.pkg_version

    config = Configuration()
    options: types.ConfigurationOptions

    visitors: ClassVar[Sequence[VisitorClass]] = (
        *general.GENERAL_PRESET,
        *complexity.COMPLEXITY_PRESET,
        *tokens.TOKENS_PRESET,
    )

    def __init__(
        self,
        tree: ast.AST,
        file_tokens: Sequence[tokenize.TokenInfo],
        filename: str = constants.STDIN,
    ) -> None:
        """
        Creates new checker instance.

        These parameter names should not be changed.
        ``flake8`` has special API that passes concrete parameters to
        the plugins that ask for them.

        ``flake8`` also decides how to execute this plugin
        based on its parameters. This one is executed once per module.

        Parameters:
            tree: ``ast`` parsed by ``flake8``.
                Differs from ``ast.parse`` since it is mutated by multiple
                ``flake8`` plugins. Why mutated? Since it is really expensive
                to copy all ``ast`` information in terms of memory.

            file_tokens: ``tokenize.tokenize`` parsed file tokens.
            filename: module file name, might be empty if piping is used.

        """
        self.tree = transform(tree)
        self.filename = filename
        self.file_tokens = file_tokens

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """
        ``flake8`` api method to register new plugin options.

        See :class:`wemake_python_styleguide.options.config.Configuration`
        docs for detailed options reference.

        Arguments:
            parser: ``flake8`` option parser instance.

        """
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options: types.ConfigurationOptions) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = validate_options(options)

    def _run_checks(
        self,
        visitors: Sequence[VisitorClass],
    ) -> Iterator[types.CheckResult]:
        """Runs all passed visitors one by one."""
        for visitor_class in visitors:
            visitor = visitor_class.from_checker(self)
            visitor.run()

            for error in visitor.violations:
                yield (*error.node_items(), type(self))

    def run(self) -> Iterator[types.CheckResult]:
        """
        Runs the checker.

        This method is used by ``flake8`` API.
        It is executed after all configuration is parsed.

        Yields:
            Violations that were found by the passed visitors.

        """
        yield from self._run_checks(self.visitors)
