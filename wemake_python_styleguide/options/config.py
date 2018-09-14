# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union

import attr
from flake8.options.manager import OptionManager

from wemake_python_styleguide.options import defaults

ConfigValues = Dict[str, Union[str, int, bool]]


@attr.attrs(frozen=True, auto_attribs=True, slots=True)
class _Option(object):
    """This class represent `flake8` option object."""

    long_option_name: str
    default: int  # noqa: E704
    help: str
    type: str = 'int'  # noqa: A003
    parse_from_config: bool = True


class Configuration(object):
    """
    Provides configuration options for ``wemake-python-styleguide`` plugin.

    You can adjust configuration via CLI option:

    Example::

        flake8 --max-returns 7

    You can also provide configuration options in ``tox.ini`` or ``setup.cfg``:

    Example::

        [flake8]
        max-returns = 7

    We support the following options:

    - ``max-returns`` - maximum allowed number of ``return``
      statements in one function, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_RETURNS`
    - ``max-local-variables`` - maximum allowed number of local
      variables in one function, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_LOCAL_VARIABLES`
    - ``max-expressions`` - maximum allowed number of expressions
      in one function, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_EXPRESSIONS`
    - ``max-arguments`` - maximum allowed number of arguments in one function,
      defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_ARGUMENTS`
    - ``min-variable-length`` - minimum number of chars to define a valid
      variable name, defaults to
      :str:`wemake_python_styleguide.options.defaults.MIN_VARIABLE_LENGTH`
    - ``max-offset-blocks`` - maximum number of block to nest expressions,
      defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_OFFSET_BLOCKS`
    - ``max-elifs`` - maximum number of ``elif`` blocks, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_ELIFS`
    - `max-module-members` - maximum number of classes and functions
      in a single module, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_MODULE_MEMBERS`
    - ``max-methods`` - maximum number of methods in a single class,
      defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_METHODS`
    - ``min-module-name-length`` - minimum required module's name length,
      defaults to
      :str:`wemake_python_styleguide.options.defaults.MIN_MODULE_NAME_LENGTH`
    - ``max-line-complexity`` - maximum line complexity measured in number of
      ``ast`` nodes per line, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_LINE_COMPLEXITY`
    - ``max-jones-score`` - maximum Jones score for a module, which is equal
      to the median of all lines complexity sum, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_JONES_SCORE`

    """

    @classmethod
    def all_options(cls) -> Sequence[_Option]:
        """Returns a list of option values we use in this plugin."""
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
                '--max-elifs',
                defaults.MAX_ELIFS,
                'Maximum number of `elif` blocks.',
            ),

            _Option(
                '--max-module-members',
                defaults.MAX_MODULE_MEMBERS,
                'Maximum number of classes and functions in a single module.',
            ),

            _Option(
                '--max-methods',
                defaults.MAX_METHODS,
                'Maximum number of methods in a single class.',
            ),

            _Option(
                '--min-module-name-length',
                defaults.MIN_MODULE_NAME_LENGTH,
                "Minimum required module's name length",
            ),

            _Option(
                '--max-line-complexity',
                defaults.MAX_LINE_COMPLEXITY,
                'Maximum line complexity, measured in `ast` nodes.',
            ),

            _Option(
                '--max-jones-score',
                defaults.MAX_JONES_SCORE,
                'Maximum median module complexity, based on sum of lines.',
            ),
        ]

    def register_options(self, parser: OptionManager) -> None:
        """Registers options for our plugin."""
        for option in self.all_options():
            parser.add_option(**attr.asdict(option))
