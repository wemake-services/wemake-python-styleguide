# -*- coding: utf-8 -*-

from wemake_python_styleguide.options import defaults


class Configuration(object):
    """Provides method for registering options for Z flake8 plugin."""

    def register_options(self, parser):
        """Registers options for Z plugin."""
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
