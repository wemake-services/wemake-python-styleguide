# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union

import attr
from flake8.options.manager import OptionManager

from wemake_python_styleguide.options import defaults

ConfigValues = Dict[str, Union[str, int, bool]]


@attr.attrs(frozen=True, auto_attribs=True, slots=True)
class Option(object):
    """This class represent `flake8` option object."""

    long_option_name: str
    default: int  # noqa: E704
    help: str
    type: str = 'int'  # noqa: A003
    parse_from_config: bool = True


class Configuration(object):
    """
    Provides configuration options for `wemake-python-styleguide` plugin.

    You can adjust configuration via CLI option:

    Example::

        flake8 --max-returns 7

    You can also provide configuration options in `tox.ini` or `setup.cfg`:

    Example::

        [flake8]
        max-returns = 7

    We support the following options:

    - `max-returns` - maximum allowed number of ``return``
      statements in one function, defaults to ``MAX_RETURNS``
    - `max-local-variables` - maximum allowed number of local
      variables in one function, defaults to ``MAX_LOCAL_VARIABLES``
    - `max-expressions` - maximum allowed number of expressions
      in one function, defaults to ``MAX_EXPRESSIONS``
    - `max-arguments` - maximum allowed number of arguments in one function,
      defaults to ``MAX_ARGUMENTS``
    - `min-variable-length` - minimum number of chars to define a valid
      variable name, defaults to ``MIN_VARIABLE_LENGTH``
    - `max-offset-blocks` - maximum number of block to nest expressions,
      defaults to ``MAX_OFFSET_BLOCKS``
    - `max-elifs` - maximum number of `elif` blocks, defaults to ``MAX_ELIFS``
    - `max-module-members` - maximum number of classes and functions
      in a single module, defaults to ``MAX_MODULE_MEMBERS``
    - `max-methods` - maximum number of methods in a single class,
      defaults to ``MAX_METHODS``
    - `min-module-name-length` - minimum required module's name length,
      defaults to ``MIN_MODULE_NAME_LENGTH``

    """

    def _all_options(self) -> Sequence[Option]:
        return [
            Option(
                '--max-returns',
                defaults.MAX_RETURNS,
                'Maximum allowed number of return statements in one function.',
            ),

            Option(
                '--max-local-variables',
                defaults.MAX_LOCAL_VARIABLES,
                'Maximum allowed number of local variables in one function.',
            ),

            Option(
                '--max-expressions',
                defaults.MAX_EXPRESSIONS,
                'Maximum allowed number of expressions in one function.',
            ),

            Option(
                '--max-arguments',
                defaults.MAX_ARGUMENTS,
                'Maximum allowed number of arguments in one function.',
            ),

            Option(
                '--min-variable-length',
                defaults.MIN_VARIABLE_LENGTH,
                'Minimum required length of the variable name.',
            ),

            Option(
                '--max-offset-blocks',
                defaults.MAX_OFFSET_BLOCKS,
                'Maximum number of blocks to nest different structures.',
            ),

            Option(
                '--max-elifs',
                defaults.MAX_ELIFS,
                'Maximum number of `elif` blocks.',
            ),

            Option(
                '--max-module-members',
                defaults.MAX_MODULE_MEMBERS,
                'Maximum number of classes and functions in a single module.',
            ),

            Option(
                '--max-methods',
                defaults.MAX_METHODS,
                'Maximum number of methods in a single class.',
            ),

            Option(
                '--min-module-name-length',
                defaults.MIN_MODULE_NAME_LENGTH,
                "Minimum required module's name length",
            ),
        ]

    def register_options(self, parser: OptionManager) -> None:
        """Registers options for our plugin."""
        options = self._all_options()
        for option in options:
            parser.add_option(**attr.asdict(option))
