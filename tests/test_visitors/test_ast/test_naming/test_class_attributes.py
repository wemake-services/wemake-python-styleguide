import pytest

from wemake_python_styleguide.logic.naming import enums
from wemake_python_styleguide.violations.naming import (
    UpperCaseAttributeViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

static_attribute = """
class Test:
    {0} = None
"""

static_typed_attribute = """
class Test:
    {0}: int = None
"""

static_typed_condition_attribute = """
class Test:
    if sys.version_info > (3, 'whatever'):
        {0}: int = None
"""

regression423 = """
class MyClass:
    def action_method(self, request, second):
        ...

    action_method.label = 'Do action'
"""

static_attribute_with_base_template = """
class Test({0}):
    {1}
"""

upper_case_attributes = [
    'UPPER: str = 1',
    'UPPER_CASE = ...',
    'lower = UPPER = auto()',
    'lower, UPPER = field',
]

custom_enum_base_class = """
class BaseEnum(enum.Enum):
    def __init__(self, short: str, long: str) -> None:
        self.short = short
        self.long = long

class ConcreteEnum(BaseEnum):
    HELLO = 'h', 'hello'
    WORLD = 'w', 'world'
"""


multiple_custom_enum_bases = """
class FirstEnum(enum.Enum):
    pass

class SecondEnum(enum.Enum):
    pass

class FirstEnumSuccessor(FirstEnum):
    HELLO = 'hello'
    WORLD = 'world'

class SecondEnumSuccessor(SecondEnum):
    PING = 'pong'

class MultiInheritanceEnum(FirstEnum, SecondEnum):
    MULTI = 'multi'
"""

dotted_names_enum_bases = """
from src import constants

class FirstEnum(constants.MyEnum):
    HELLO = 'hello'
    WORLD = 'world'

class SecondEnum(constants.MyEnum):
    HELLO = 'hello'
    WORLD = 'world'
"""


@pytest.mark.parametrize(
    'code',
    [
        static_attribute,
        static_typed_attribute,
        static_typed_condition_attribute,
    ],
)
@pytest.mark.parametrize(
    'non_snake_case_name',
    [
        'Abc',
        'A_CONSTANT',
        'AAA',
        'B2',
        'CONST1_bc',
        'camelCase',
        '_A_c',
    ],
)
def test_upper_case_class_attributes(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    non_snake_case_name,
    code,
    default_options,
):
    """Testing that attribute cannot have too short names."""
    tree = parse_ast_tree(code.format(non_snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UpperCaseAttributeViolation])
    assert_error_text(visitor, non_snake_case_name)


@pytest.mark.parametrize(
    'base_class',
    enums._ENUM_LIKE_NAMES,  # noqa: SLF001
)
@pytest.mark.parametrize(
    'attribute',
    [
        *upper_case_attributes,
        'lower_should_pass_too: bool = True',
        'lower_should_pass_too = 1',
        'UPPER_NAME = UPPER_ALIAS = auto()',
    ],
)
def test_upper_case_enum_attributes(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    base_class,
    attribute,
    default_options,
):
    """
    Testing that enum-like classes can have UPPER_SNAKE_CASE attributes.

    These enum-like classes include not only default
    Python enums, but also Django enumerations
    """
    tree = parse_ast_tree(
        static_attribute_with_base_template.format(base_class, attribute),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'base_class',
    [
        'not_enum.Base',
        'MyAbstractFactory',
        'metaclass=MyMeta',
    ],
)
@pytest.mark.parametrize(
    'attribute',
    upper_case_attributes,
)
def test_upper_case_non_enum_attributes(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    base_class,
    attribute,
    default_options,
):
    """Testing that UPPER_CASE attributes still aren't allowed."""
    tree = parse_ast_tree(
        static_attribute_with_base_template.format(base_class, attribute),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UpperCaseAttributeViolation])


@pytest.mark.parametrize(
    'code',
    [
        static_attribute,
        static_typed_attribute,
        static_typed_condition_attribute,
    ],
)
@pytest.mark.parametrize(
    'snake_case_name',
    [
        'abc',
        'a_variable',
        'aaa',
        'two_minutes_to_midnight',
        'variable42_5',
        '_a_c',
    ],
)
def test_snake_case_class_attributes(
    assert_errors,
    parse_ast_tree,
    snake_case_name,
    code,
    default_options,
):
    """Testing that attribute cannot have too short names."""
    tree = parse_ast_tree(code.format(snake_case_name))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_regression423(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """
    Tests that this issue-423 won't happen again.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/423
    """
    tree = parse_ast_tree(regression423)

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('with_configuration', [True, False])
def test_custom_enum_base_class_with_config(
    assert_errors,
    parse_ast_tree,
    options,
    with_configuration,
):
    """Testing that custom enum base classes work with configuration."""
    tree = parse_ast_tree(custom_enum_base_class)

    if with_configuration:
        options_with_config = options(known_enum_bases=('BaseEnum',))
        visitor = WrongNameVisitor(options_with_config, tree=tree)
        visitor.run()
        assert_errors(visitor, [])
    else:
        options_without_config = options()
        visitor = WrongNameVisitor(options_without_config, tree=tree)
        visitor.run()
        assert_errors(
            visitor,
            [UpperCaseAttributeViolation, UpperCaseAttributeViolation],
        )


def test_multiple_custom_enum_bases_with_config(
    assert_errors,
    parse_ast_tree,
    options,
):
    """Testing that multiple custom enum base classes work with config."""
    tree = parse_ast_tree(multiple_custom_enum_bases)

    options = options(known_enum_bases=('FirstEnum', 'SecondEnum'))
    visitor = WrongNameVisitor(options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])


def test_dotted_names_in_enum_bases_config(
    assert_errors,
    parse_ast_tree,
    options,
):
    """Testing that dotted names in enum bases config work correctly."""
    tree = parse_ast_tree(dotted_names_enum_bases)

    options = options(known_enum_bases=('constants.MyEnum',))
    visitor = WrongNameVisitor(options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])
