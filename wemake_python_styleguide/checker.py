# -*- coding: utf-8 -*-

"""
Entry point to the app.

Writing new plugin
------------------

First of all, you have to decide:

1. Are you writing a separate plugin and adding it as a dependency?
2. Are you writing an built-in extension to this styleguide?

How to make a decision?

Will this plugin be useful to other developers without this styleguide?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If so, it would be wise to create a separate ``flake8`` plugin.
Then you can add newly created plugin as a dependency.
Our rules do not make any sense without each other.

Real world examples:

- `flake8-eradicate <https://github.com/sobolevn/flake8-eradicate>`_

Can this plugin be used with the existing checker?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``flake8`` has a very strict API about plugins.
Here are some problems that you may encounter:

- Some plugins are called once per file, some are called once per line
- Plugins should define clear ``violation code`` / ``checker`` relation
- It is impossible to use the same letter violation codes for several checkers

Real world examples:

- `flake8-broken-line <https://github.com/sobolevn/flake8-broken-line>`_

Writing new visitor
-------------------

If you are still willing to write a builtin extension to our styleguide,
you will have to write a :ref:`violation <violations>`
and/or :ref:`visitor <visitors>`.

Checker API
-----------

.. autoclass:: Checker
   :members:
   :special-members:
   :exclude-members: __weakref__

"""

import ast
import tokenize
from typing import ClassVar, Iterator, Sequence, Type

from flake8.options.manager import OptionManager

from wemake_python_styleguide import constants, types
from wemake_python_styleguide import version as pkg_version
from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.transformations.ast_tree import transform
from wemake_python_styleguide.visitors import base
from wemake_python_styleguide.visitors.presets import (
    complexity,
    general,
    tokens,
)

VisitorClass = Type[base.BaseVisitor]


@types.final
class Checker(object):
    """
    Main checker class.

    It is an entry point to the whole app.

    Attributes:
        name: required by the ``flake8`` API, should match the package name.
        version: required by the ``flake8`` API, defined in the packaging file.
        config: custom configuration object used to provide and parse options.
        options: option structure passed by ``flake8``.
        visitors: sequence of visitors that we run with this checker.

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
            tree: ``ast`` parsed by ``flake8``. Differs from ``ast.parse``.
            file_tokens: ``tokenize.tokenize`` parsed file tokens.
            filename: module file name, might be empty if piping is used.

        See also:
            http://flake8.pycqa.org/en/latest/plugin-development/index.html

        """
        self.tree = transform(tree)
        self.filename = filename
        self.file_tokens = file_tokens

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """
        ``flake8`` api method to register new plugin options.

        See :class:`.Configuration` docs for detailed options reference.

        Arguments:
            parser: ``flake8`` option parser instance.

        """
        cls.config.register_options(parser)

    @classmethod
    def parse_options(cls, options: types.ConfigurationOptions) -> None:
        """Parses registered options for providing them to each visitor."""
        cls.options = options

    def _run_checks(
        self,
        visitors: Sequence[VisitorClass],
    ) -> Iterator[types.CheckResult]:
        """
        Runs all passed visitors one by one.

        Yields:
            Violations that were found by the passed visitors.

        """
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
        """
        yield from self._run_checks(self.visitors)
