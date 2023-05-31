"""
Provides configuration options for ``wemake-python-styleguide``.

We do not like our linter to be highly configurable.
Since, people may take the wrong path or make wrong decisions.
We try to make all defaults as reasonable as possible.

However, you can currently adjust some complexity options. Why?
Because we are not quite sure about the ideal values.

All options are configurable via ``flake8`` CLI.

.. code:: ini

    flake8 --max-returns=2 --max-arguments=4

Or you can provide options in ``setup.cfg`` or similar supported files.

.. code:: ini

    [flake8]
    max-returns = 2
    max-arguments = 4

We use ``setup.cfg`` as a default way to provide configuration.

You can also show all options that ``flake8`` supports by running:

.. code:: bash

    flake8 --help

.. rubric:: General options

- ``min-name-length`` - minimum number of chars to define a valid
    variable and module name, defaults to
    :str:`wemake_python_styleguide.options.defaults.MIN_NAME_LENGTH`
- ``max-name-length`` - maximum number of chars to define a valid
    variable and module name, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_NAME_LENGTH`
- ``i-control-code`` - whether you control ones who use your code,
    more rules are enforced when you do control it,
    opposite to ``--i-dont-control-code``, defaults to
    :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`
- ``i-dont-control-code`` - whether you control ones who use your code,
    more rules are enforced when you do control it,
    opposite to ``--i-control-code``, defaults to
    :str:`wemake_python_styleguide.options.defaults.I_CONTROL_CODE`
- ``nested-classes-whitelist`` - list of nested classes' names we allow to use,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.NESTED_CLASSES_WHITELIST`
- ``max-noqa-comments`` - maximum number of `noqa` allowed in a module,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_NOQA_COMMENTS`
- ``allowed-domain-names`` - list of allowed domain names, defaults to
    :str:`wemake_python_styleguide.options.defaults.ALLOWED_DOMAIN_NAMES`
- ``forbidden-domain-names`` - list of forbidden domain names, defaults to
    :str:`wemake_python_styleguide.options.defaults.FORBIDDEN_DOMAIN_NAMES`
- ``forbidden-inline-ignore`` - list of codes of violations or
    class of violations that are forbidden to ignore inline, defaults to
    :str:`wemake_python_styleguide.options.defaults.FORBIDDEN_INLINE_IGNORE`
- ``exps-for-one-empty-line`` - number of expressions in
    function or method body for available empty line (without code)
    :str:`wemake_python_styleguide.options.defaults.EXPS_FOR_ONE_EMPTY_LINE`


.. rubric:: Complexity options

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
- ``max-module-members`` - maximum number of classes and functions
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
- ``max-imports`` - maximum number of imports in a single module,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_IMPORTS`
- ``max-imported-names`` - maximum number of imported names
    in a single module, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_IMPORTED_NAMES`
- ``max-base-classes`` - maximum number of parent classes inside a class
    definition, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_BASE_CLASSES`
- ``max-decorators`` - maximum number of decorators for single function
    or class definition, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_DECORATORS`
- ``max-string-usages`` - maximum number of repeated String constants
    in your modules, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_STRING_USAGES`
- ``max-awaits`` - maximum allowed number of ``await``
    expressions in one function, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_AWAITS`
- ``max-try-body-length`` - maximum amount of ``try`` node body length,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_TRY_BODY_LENGTH`
- ``max-module-expressions`` - maximum number of expression
    usages in a module, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_MODULE_EXPRESSIONS`
- ``max-function-expressions`` - maximum number of expression
    usages in a function or method, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_FUNCTION_EXPRESSIONS`
- ``max-asserts`` - maximum number of ``assert`` statements in a function,
    default to
    :str:`wemake_python_styleguide.options.defaults.MAX_ASSERTS`
- ``max-access-level`` - maximum number of access level in an expression,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_ACCESS_LEVEL`
- ``max-attributes`` - maximum number of public instance attributes,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_ATTRIBUTES`
- ``max-raises`` - maximum number of raises in a function,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_RAISES`
- ``max-cognitive-score`` - maximum amount of cognitive complexity
    per function, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_COGNITIVE_SCORE`
- ``max-cognitive-average`` - maximum amount of cognitive complexity
    per module, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_COGNITIVE_AVERAGE`
    :str:`wemake_python_styleguide.options.defaults.NESTED_CLASSES_WHITELIST`
- ``max-call-level`` - maximum number of call chains, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_CALL_LEVEL`
- ``max-annotation-complexity`` - maximum number of nested annotations,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_ANN_COMPLEXITY`
- ``max-import-from-members`` - maximum number of names that can be imported
    from module, defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_IMPORT_FROM_MEMBERS`
- ``max-tuple-unpack-length`` - maximum number of variables in tuple unpacking,
    defaults to
    :str:`wemake_python_styleguide.options.defaults.MAX_TUPLE_UNPACK_LENGTH`

.. rubric:: Formatter options

- ``show-violation-links`` - whether to show violation shortlinks in the
    formatter output
    :str:`wemake_python_styleguide.options.defaults.SHOW_VIOLATION_LINKS`
"""

from typing import ClassVar, Mapping, Optional, Sequence, Union

import attr
from flake8.options.manager import OptionManager
from typing_extensions import Final, TypeAlias, final

from wemake_python_styleguide.options import defaults

_Type: TypeAlias = type
ConfigValuesTypes: TypeAlias = Union[str, int, bool, Sequence[str]]
String: Final = str


@final
@attr.dataclass(frozen=True, slots=True)
class _Option(object):
    """Represents ``flake8`` option object."""

    long_option_name: str
    default: ConfigValuesTypes
    help: str  # noqa: WPS125
    type: Optional[_Type] = int  # noqa: WPS125
    parse_from_config: bool = True
    action: str = 'store'
    comma_separated_list: bool = False
    dest: Optional[str] = None

    def __attrs_post_init__(self):
        """Is called after regular init is done."""
        object.__setattr__(  # noqa: WPS609
            self, 'help', ' '.join(
                (self.help, 'Defaults to: %(default)s'),  # noqa: WPS323
            ),
        )

    def asdict_no_none(self) -> Mapping[str, ConfigValuesTypes]:
        """We need this method to return options, but filter out ``None``."""
        return {
            key: opt
            for key, opt in attr.asdict(self).items()
            if opt is not None
        }


@final
class Configuration(object):
    """Simple configuration store with all options."""

    _options: ClassVar[Sequence[_Option]] = [
        # General:

        _Option(
            '--min-name-length',
            defaults.MIN_NAME_LENGTH,
            'Minimum required length of variable and module names.',
        ),
        _Option(
            '--max-name-length',
            defaults.MAX_NAME_LENGTH,
            'Maximum possible length of the variable and module names.',
        ),
        _Option(
            '--i-control-code',
            defaults.I_CONTROL_CODE,
            'Whether you control ones who use your code.',
            action='store_true',
            type=None,
            dest='i_control_code',
        ),
        _Option(
            '--i-dont-control-code',
            defaults.I_CONTROL_CODE,
            'Whether you control ones who use your code.',
            action='store_false',
            type=None,
            dest='i_control_code',
            parse_from_config=False,
        ),
        _Option(
            '--max-noqa-comments',
            defaults.MAX_NOQA_COMMENTS,
            'Maximum amount of `noqa` comments per module.',
        ),
        _Option(
            '--nested-classes-whitelist',
            defaults.NESTED_CLASSES_WHITELIST,
            'List of nested classes names we allow to use.',
            type=String,
            comma_separated_list=True,
        ),
        _Option(
            '--allowed-domain-names',
            defaults.ALLOWED_DOMAIN_NAMES,
            "Domain names that are removed from variable names' blacklist.",
            type=String,
            comma_separated_list=True,
        ),
        _Option(
            '--forbidden-domain-names',
            defaults.FORBIDDEN_DOMAIN_NAMES,
            "Domain names that extends variable names' blacklist.",
            type=String,
            comma_separated_list=True,
        ),
        _Option(
            '--forbidden-inline-ignore',
            defaults.FORBIDDEN_INLINE_IGNORE,
            'Codes of violations or class of violations forbidden to ignore.',
            type=String,
            comma_separated_list=True,
        ),
        _Option(
            '--exps-for-one-empty-line',
            defaults.EXPS_FOR_ONE_EMPTY_LINE,
            'Count of expressions for one empty line in a function body.',
        ),

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
            '--max-imported-names',
            defaults.MAX_IMPORTED_NAMES,
            'Maximum number of imported names in a single module.',
        ),
        _Option(
            '--max-base-classes',
            defaults.MAX_BASE_CLASSES,
            'Maximum number of base classes.',
        ),
        _Option(
            '--max-decorators',
            defaults.MAX_DECORATORS,
            'Maximum number of decorators.',
        ),
        _Option(
            '--max-string-usages',
            defaults.MAX_STRING_USAGES,
            'Maximum number of string constant usages.',
        ),
        _Option(
            '--max-awaits',
            defaults.MAX_AWAITS,
            'Maximum allowed number of await expressions in one function.',
        ),
        _Option(
            '--max-try-body-length',
            defaults.MAX_TRY_BODY_LENGTH,
            'Maximum amount of try block node body length.',
        ),
        _Option(
            '--max-module-expressions',
            defaults.MAX_MODULE_EXPRESSIONS,
            'Maximum amount of expression usages in a module.',
        ),
        _Option(
            '--max-function-expressions',
            defaults.MAX_FUNCTION_EXPRESSIONS,
            'Maximum amount of expression usages in a function or method.',
        ),
        _Option(
            '--max-asserts',
            defaults.MAX_ASSERTS,
            'Maximum allowed number of assert statements in one function.',
        ),
        _Option(
            '--max-access-level',
            defaults.MAX_ACCESS_LEVEL,
            'Maximum number of access level in an expression.',
        ),
        _Option(
            '--max-attributes',
            defaults.MAX_ATTRIBUTES,
            'Maximum number of public instance attributes.',
        ),
        _Option(
            '--max-raises',
            defaults.MAX_RAISES,
            'Maximum number of raises in a function.',
        ),
        _Option(
            '--max-cognitive-score',
            defaults.MAX_COGNITIVE_SCORE,
            'Maximum amount of cognitive complexity per function.',
        ),
        _Option(
            '--max-cognitive-average',
            defaults.MAX_COGNITIVE_AVERAGE,
            'Maximum amount of average cognitive complexity per module.',
        ),
        _Option(
            '--max-call-level',
            defaults.MAX_CALL_LEVEL,
            'Maximum number of call chains.',
        ),
        _Option(
            '--max-annotation-complexity',
            defaults.MAX_ANN_COMPLEXITY,
            'Maximum number of nested annotations.',
        ),
        _Option(
            '--max-import-from-members',
            defaults.MAX_IMPORT_FROM_MEMBERS,
            'Maximum number of names that can be imported from module.',
        ),
        _Option(
            '--max-tuple-unpack-length',
            defaults.MAX_TUPLE_UNPACK_LENGTH,
            'Maximum number of variables in a tuple unpacking.',
        ),

        # Formatter:

        _Option(
            '--show-violation-links',
            defaults.SHOW_VIOLATION_LINKS,
            'Whether to show violation shortlinks in the formatter output.',
            action='store_true',
            type=None,
            dest='show_violation_links',
        ),
    ]

    def register_options(self, parser: OptionManager) -> None:
        """Registers options for our plugin."""
        for option in self._options:
            parser.add_option(**option.asdict_no_none())
