# -*- coding: utf-8 -*-

from wemake_python_styleguide.options import defaults


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

    # TODO: this function should be refactored some-how:
    # TODO: add types
    def register_options(self, parser) -> None:
        """Registers options for our plugin."""
        parser.add_option(
            '--max-returns',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_RETURNS,
            help='Maximum allowed number of return statements in one function.',
        )

        parser.add_option(
            '--max-local-variables',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_LOCAL_VARIABLES,
            help='Maximum allowed number of local variables in one function.',
        )

        parser.add_option(
            '--max-expressions',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_EXPRESSIONS,
            help='Maximum allowed number of expressions in one function.',
        )

        parser.add_option(
            '--max-arguments',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_ARGUMENTS,
            help='Maximum allowed number of arguments in one function.',
        )

        parser.add_option(
            '--min-variable-length',
            parse_from_config=True,
            type='int',
            default=defaults.MIN_VARIABLE_LENGTH,
            help='Minimum required length of the variable name.',
        )

        parser.add_option(
            '--max-offset-blocks',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_OFFSET_BLOCKS,
            help='Maximum number of blocks to nest different structures.',
        )

        parser.add_option(
            '--max_elifs',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_ELIFS,
            help='Maximum number of `elif` blocks.',
        )

        parser.add_option(
            '--max_module_members',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_MODULE_MEMBERS,
            help='Maximum number of classes and functions in a single module.',
        )

        parser.add_option(
            '--max_methods',
            parse_from_config=True,
            type='int',
            default=defaults.MAX_METHODS,
            help='Maximum number of methods in a single class.',
        )
