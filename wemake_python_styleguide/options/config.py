# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union

from flake8.options.manager import OptionManager

from wemake_python_styleguide.options import defaults


class _Option(object):
    """This class represent `flake8` option object."""

    def __init__(
        self,
        name: str,
        default_value: int,
        help_text: str,
        option_type: type = int,
        parse_from_config: bool = True,
    ) -> None:
        self.name = name
        self.default_value = default_value
        self.help_text = help_text
        self.option_type = option_type
        self.parse_from_config = parse_from_config

    def to_option(self) -> Dict[str, Union[str, int, type]]:
        return {
            'parse_from_config': self.parse_from_config,
            'type': self.option_type,
            'default': self.default_value,
            'help': self.help_text,
        }


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
    - `max_offset_blocks` - maximum number of block to nest expressions,
      defaults to ``MAX_OFFSET_BLOCKS``
    - `max_elifs` - maximum number of `elif` blocks, defaults to ``MAX_ELIFS``
    - `max_module_members` - maximum number of classes and functions
      in a single module, defaults to ``MAX_MODULE_MEMBERS``
    - `max_methods` - maximum number of methods in a single class,
      defaults to ``MAX_METHODS``

    """

    def _all_options(self) -> Sequence[_Option]:
        return [
            _Option(
                '--max-returns',
                defaults.MAX_RETURNS,
                'Maximum allowed number of return statements in one function.',
            ),

            _Option(
                '--max-local-variables',
                defaults.MAX_LOCAL_VARIABLES,
                'Maximum allowed number of local variables in one function.',
            ),

            _Option(
                '--max-expressions',
                defaults.MAX_EXPRESSIONS,
                'Maximum allowed number of expressions in one function.',
            ),

            _Option(
                '--max-arguments',
                defaults.MAX_ARGUMENTS,
                'Maximum allowed number of arguments in one function.',
            ),

            _Option(
                '--min-variable-length',
                defaults.MIN_VARIABLE_LENGTH,
                'Minimum required length of the variable name.',
            ),

            _Option(
                '--max-offset-blocks',
                defaults.MAX_OFFSET_BLOCKS,
                'Maximum number of blocks to nest different structures.',
            ),

            _Option(
                '--max_elifs',
                defaults.MAX_ELIFS,
                'Maximum number of `elif` blocks.',
            ),

            _Option(
                '--max_module_members',
                defaults.MAX_MODULE_MEMBERS,
                'Maximum number of classes and functions in a single module.',
            ),

            _Option(
                '--max_methods',
                defaults.MAX_METHODS,
                'Maximum number of methods in a single class.',
            ),
        ]

    def register_options(self, parser: OptionManager) -> None:
        """Registers options for our plugin."""
        options = self._all_options()
        for option in options:
            parser.add_option(option.name, **option.to_option())
