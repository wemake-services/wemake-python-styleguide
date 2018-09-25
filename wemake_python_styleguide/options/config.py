# -*- coding: utf-8 -*-

from typing import Dict, Optional, Sequence, Union

import attr
from flake8.options.manager import OptionManager

from wemake_python_styleguide.options import defaults

ConfigValues = Dict[str, Union[str, int, bool]]


@attr.attrs(frozen=True, auto_attribs=True, slots=True)
class _Option(object):
    """Represents ``flake8`` option object."""

    long_option_name: str
    default: int  # noqa: E704
    help: str
    type: Optional[str] = 'int'  # noqa: A003
    parse_from_config: bool = True
    action: str = 'store'


class Configuration(object):
    """
    Provides configuration options for our plugin.

    We do not like our linter to be configurable.
    Since people may take the wrong path or make wrong decisions.
    We try to make all defaults as reasonable as possible.

    However, you can currently adjust some complexity options. Why?
    Because we are quite sure about the ideal values. We are still researching
    them, and providing a way for developers to help us out is a good thing
    at the moment.

    Options for general checks:

    - ``min-variable-length`` - minimum number of chars to define a valid
      variable name, defaults to
      :str:`wemake_python_styleguide.options.defaults.MIN_VARIABLE_LENGTH`
    - ``i-control-code`` - either or not your control ones who use your code,
      more rule are enforced when you do control it, defaults to
      :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`

    Options for module names related checks:

    - ``min-module-name-length`` - minimum required module's name length,
      defaults to
      :str:`wemake_python_styleguide.options.defaults.MIN_MODULE_NAME_LENGTH`

    Options for complexity related checks:

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
    - ``max-line-complexity`` - maximum line complexity measured in number of
      ``ast`` nodes per line, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_LINE_COMPLEXITY`
    - ``max-jones-score`` - maximum Jones score for a module, which is equal
      to the median of all lines complexity sum, defaults to
      :str:`wemake_python_styleguide.options.defaults.MAX_JONES_SCORE`

    All options are configurable via ``flake8`` CLI:

    Example::

        flake8 --max-returns 7

    Or you can provide options in ``tox.ini`` or ``setup.cfg``:

    Example::

        [flake8]
        max-returns = 7

    We use ``setup.cfg`` as a default way to provide configuration.

    """

    #: List of option values we use in this plugin:
    options: Sequence[_Option] = [

        # Complexity:

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
            '--max-line-complexity',
            defaults.MAX_LINE_COMPLEXITY,
            'Maximum line complexity, measured in `ast` nodes.',
        ),

        _Option(
            '--max-jones-score',
            defaults.MAX_JONES_SCORE,
            'Maximum median module complexity, based on sum of lines.',
        ),

        _Option(
            '--max-imports',
            defaults.MAX_IMPORTS,
            'Maximum number of imports in a single module.',
        ),

        _Option(
            '--max-conditions',
            defaults.MAX_CONDITIONS,
            'Maximum number of conditions in a `if` or `while` node.',
        ),

        # General:

        _Option(
            '--min-variable-length',
            defaults.MIN_VARIABLE_LENGTH,
            'Minimum required length of the variable name.',
        ),

        _Option(
            '--i-control-code',
            defaults.I_CONTROL_CODE,
            'Either or not you control ones who use your code.',
            action='store_true',
            type=None,
        ),

        # File names:

        _Option(
            '--min-module-name-length',
            defaults.MIN_MODULE_NAME_LENGTH,
            "Minimum required module's name length",
        ),
    ]

    def register_options(self, parser: OptionManager) -> None:
        """Registers options for our plugin."""
        for option in self.options:
            parser.add_option(**attr.asdict(option))
