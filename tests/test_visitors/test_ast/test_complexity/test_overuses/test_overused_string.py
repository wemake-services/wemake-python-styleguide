import pytest

from wemake_python_styleguide.compat.constants import PY312, PY314
from wemake_python_styleguide.violations.complexity import (
    OverusedStringViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.overuses import (
    StringOveruseVisitor,
)

_USAGE_COUNT = 5

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
class SomeClass:
    first: {0}
    second: {0}
    third: {0}
    fourth: {0}
"""

string_method_type_annotations1 = """
class SomeClass:
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
class SomeClass:
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

class Some:
    field: {0}

    def method(self, arg: {0}):
        ...

def function() -> Dict[int, {0}]:
    ...
"""

fstring_same_prefix1 = """
x = f'Hello, {pattern}'
y = f'Hello, {pattern}'
"""

fstring_same_prefix2 = """
x = f'{pattern}-postfix'
y = f'{pattern}-postfix'
"""

tstring_same_prefix1 = pytest.param(
    """
    x = t'Hello, {pattern}'
    y = t'Hello, {pattern}'
    """,
    marks=pytest.mark.skipif(
        not PY314,
        reason='t-strings are only in Python 3.14+',
    ),
)

tstring_same_prefix2 = pytest.param(
    """
    x = t'{pattern}-postfix'
    y = t'{pattern}-postfix'
    """,
    marks=pytest.mark.skipif(
        not PY314,
        reason='t-strings are only in Python 3.14+',
    ),
)

# See:
# https://github.com/wemake-services/wemake-python-styleguide/issues/3803
module_docstring = """
{0}
"""

function_docstrings = """
def first():
    {0}

def second():
    {0}

class Some:
    {0}

    def method(self):
        {0}
"""

not_a_docstring = '''
def first():
    """Docs."""
    {0}

def second():
    """Docs."""
    {0}

def third():
    """Docs."""
    {0}

def fourth():
    """Docs."""
    {0}
'''

# See:
# https://github.com/wemake-services/wemake-python-styleguide/issues/3805
module_attribute_docstrings = """
first = 1
{0}

second: int = 2
{0}

third: int
{0}
"""

class_attribute_docstrings = """
class Some:
    first = 1
    {0}

    second: int = 2
    {0}

    def __init__(self):
        self.third = 3
        {0}
"""

not_an_attribute_docstring = """
def first():
    print(1)
    {0}

def second():
    print(2)
    {0}

def third():
    print(3)
    {0}

def fourth():
    x = 1
    {0}
"""

# Type aliases are documented the very same way, see:
# https://discuss.python.org/t/docstrings-for-type-aliases/108901
explicit_type_alias_docstrings = """
Timeout: TypeAlias = float
{0}

Retries: TypeAlias = int
{0}

Backoff: TypeAlias = float
{0}
"""

type_alias_docstrings = pytest.param(
    """
    type Timeout = float | None
    {0}

    type Retries = int
    {0}

    type Backoff = float
    {0}
    """,
    marks=pytest.mark.skipif(
        not PY312,
        reason='`type` aliases are only in Python 3.12+',
    ),
)

EXPECTED_LOCATION = (2, 8)


@pytest.mark.parametrize(
    'strings',
    [
        string_actions,
        string_function_type_annotations1,
        string_function_type_annotations2,
        string_class_type_annotations,
        string_method_type_annotations1,
        string_method_type_annotations2,
        string_variable_type_annotations,
        regression1127,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"same_string"',
        '"GenericType[int, str]"',
    ],
)
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


@pytest.mark.parametrize(
    'strings',
    [
        string_actions,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"same-string"',
        '"GenericType[int, str]"',
        '"{0}"',
    ],
)
@pytest.mark.parametrize(
    'prefix',
    [
        'b',
        'u',
        '',
    ],
)
def test_string_overuse(
    assert_errors,
    assert_error_text,
    assert_error_location,
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

    string_value = string_value.replace('"', '')
    assert_error_text(
        visitor,
        f'{string_value!r} {_USAGE_COUNT}',
        default_options.max_string_usages,
    )
    assert_error_location(visitor, EXPECTED_LOCATION)


@pytest.mark.parametrize(
    'strings',
    [
        string_actions,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"same-string"',
        '"GenericType[int, str]"',
        '"{0}"',
    ],
)
def test_string_overuse_bytes_and_str(
    assert_errors,
    parse_ast_tree,
    default_options,
    strings,
    string_value,
):
    """Ensures that string and bytes are treated separately."""
    bytes_value = f'b{string_value}'
    tree = parse_ast_tree(
        strings.format(bytes_value) + strings.format(string_value),
    )
    visitor = StringOveruseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedStringViolation, OverusedStringViolation])


@pytest.mark.parametrize(
    'strings',
    [
        string_function_type_annotations1,
        string_function_type_annotations2,
        string_class_type_annotations,
        string_method_type_annotations1,
        string_method_type_annotations2,
        string_variable_type_annotations,
        regression1127,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"GenericType[int, str]"',
        '"int"',
        'List["int"]',
        'list[int]',
        'int | None',
    ],
)
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


@pytest.mark.parametrize(
    'string_value',
    [
        r'"\t"',
        r'"\n"',
        '""',
        '","',
        '"/"',
        '"."',
        "'\"'",
        '"\'"',
    ],
)
@pytest.mark.parametrize(
    'prefix',
    [
        'b',
        'u',
        '',
    ],
)
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


@pytest.mark.parametrize(
    'strings',
    [
        module_docstring,
        function_docstrings,
        module_attribute_docstrings,
        class_attribute_docstrings,
        explicit_type_alias_docstrings,
        type_alias_docstrings,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"""Docstring."""',
        '"Docstring."',
    ],
)
def test_docstrings_not_counted(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
):
    """Ensures that docstrings do not count against the overuse limit."""
    tree = parse_ast_tree(strings.format(string_value))

    option_values = options(max_string_usages=0)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'strings',
    [
        not_a_docstring,
        not_an_attribute_docstring,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"""Not a docstring."""',
        '"Not a docstring."',
    ],
)
def test_strings_in_other_places_counted(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
    string_value,
):
    """Ensures that strings documenting nothing are still counted."""
    tree = parse_ast_tree(strings.format(string_value))

    option_values = options(max_string_usages=0)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedStringViolation])


@pytest.mark.parametrize(
    'strings',
    [
        fstring_same_prefix1,
        fstring_same_prefix2,
        tstring_same_prefix1,
        tstring_same_prefix2,
    ],
)
def test_format_strings_not_counted(
    assert_errors,
    parse_ast_tree,
    options,
    strings,
):
    """Ensures that string literals inside f-strings are not overused."""
    tree = parse_ast_tree(strings)
    option_values = options(max_string_usages=1)
    visitor = StringOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
