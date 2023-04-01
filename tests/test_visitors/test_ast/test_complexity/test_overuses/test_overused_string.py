import pytest

from wemake_python_styleguide.violations.complexity import (
    OverusedStringViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.overuses import (
    StringOveruseVisitor,
)

string_actions = """
first = {0}
second({0})
third[{0}]
'new' + {0}
{0}.join("1", "2", "3")
"""

string_function_type_annotations1 = """
def first(
    arg1: {0},
    arg2: {0},
    arg3: {0},
    arg4: {0},
) -> {0}:
    ...
"""

string_function_type_annotations2 = """
def func1() -> {0}:
    ...

def func2() -> {0}:
    ...

def func3() -> {0}:
    ...

def func4() -> {0}:
    ...
"""

string_class_type_annotations = """
class SomeClass(object):
    first: {0}
    second: {0}
    third: {0}
    fourth: {0}
"""

string_method_type_annotations1 = """
class SomeClass(object):
    def first(
        self,
        arg1: {0},
        arg2: {0},
        arg3: {0},
        arg4: {0},
    ) -> {0}:
        ...
"""

string_method_type_annotations2 = """
class SomeClass(object):
    def method1(self) -> {0}:
        ...

    def method2(self) -> {0}:
        ...

    def method3(self) -> {0}:
        ...

    def method4(self) -> {0}:
        ...
"""

string_variable_type_annotations = """
first: {0}
second: {0}
third: {0}
fourth: {0}
"""

# See:
# https://github.com/wemake-services/wemake-python-styleguide/issues/1127
regression1127 = """
first: List[{0}]

class Some(object):
    field: {0}

    def method(self, arg: {0}):
        ...

def function() -> Dict[int, {0}]:
    ...
"""


@pytest.mark.parametrize('strings', [
    string_actions,
    string_function_type_annotations1,
    string_function_type_annotations2,
    string_class_type_annotations,
    string_method_type_annotations1,
    string_method_type_annotations2,
    string_variable_type_annotations,
    regression1127,
])
@pytest.mark.parametrize('string_value', [
    '"same_string"',
    '"GenericType[int, str]"',
])
def test_string_overuse_settings(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
    mode,
):
    """Ensures that settings for string over-use work."""
    tree = parse_ast_tree(mode(strings.format(string_value)))

    option_values = options(max_string_usages=5)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('strings', [
    string_actions,
])
@pytest.mark.parametrize('string_value', [
    '"same-string"',
    '"GenericType[int, str]"',
])
@pytest.mark.parametrize('prefix', [
    'b',
    'u',
    '',
])
def test_string_overuse(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    strings,
    prefix,
    string_value,
):
    """Ensures that over-used strings raise violations."""
    tree = parse_ast_tree(strings.format(prefix + string_value))

    visitor = StringOveruseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedStringViolation])
    assert_error_text(
        visitor,
        string_value.replace('"', '') or "''",
        default_options.max_string_usages,
    )


@pytest.mark.parametrize('strings', [
    string_function_type_annotations1,
    string_function_type_annotations2,
    string_class_type_annotations,
    string_method_type_annotations1,
    string_method_type_annotations2,
    string_variable_type_annotations,
    regression1127,
])
@pytest.mark.parametrize('string_value', [
    '"GenericType[int, str]"',
    '"int"',
    'List["int"]',
    'list[int]',
    'int | None',
])
def test_string_type_annotations(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
    mode,
):
    """Ensures that type annotations do not raise violations."""
    tree = parse_ast_tree(mode(strings.format(string_value)))

    option_values = options(max_string_usages=0)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('string_value', [
    r'"\t"',
    r'"\n"',
    '""',
    '","',
    '"."',
    "'\"'",
    '"\'"',
])
@pytest.mark.parametrize('prefix', [
    'b',
    'u',
    '',
])
def test_common_strings_allowed(
    assert_errors,
    parse_ast_tree,
    default_options,
    prefix,
    string_value,
):
    """Ensures that common strings do not count against the overuse limit."""
    snippet = string_actions.format(prefix + string_value)
    tree = parse_ast_tree(snippet)

    visitor = StringOveruseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
