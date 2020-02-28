import pytest

from wemake_python_styleguide.violations.complexity import (
    TooComplexAnnotationViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.annotations import (
    AnnotationComplexityVisitor,
)

annassign_template = 'some: {0}'

function_arg_template = """
def some(arg: {0}):
    ...
"""

function_return_template = """
def some(arg) -> {0}:
    ...
"""

class_field_template = """
class Test(object):
    some: {0}
    other = 1
"""


@pytest.mark.parametrize('template', [
    annassign_template,
    function_arg_template,
    function_return_template,
    class_field_template,
])
@pytest.mark.parametrize('code', [
    'int',
    'List[int]',
    'List["MyType"]',
    '"List[MyType]"',
    'Dict[int, str]',
    'Callable[[str, int], int]',
    'List[List[int]]',
])
def test_correct_annotations(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    mode,
    default_options,
):
    """Testing that expressions with correct call chain length work well."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = AnnotationComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    annassign_template,
    function_arg_template,
    function_return_template,
    class_field_template,
])
@pytest.mark.parametrize('code', [
    'List[List[List[int]]]',
    '"List[List[List[int]]]"',

    'Callable[[], "List[List[str]]"]',
    'Callable[[List["List[str]"]], str]',

    'Dict[int, Tuple[List[List[str]], ...]]',
    '"Dict[int, Tuple[List[List[str]], ...]]"',
    'Dict[int, "Tuple[List[List[str]], ...]"]',
    'Dict[int, Tuple["List[List[str]]", ...]]',
    'Dict[int, Tuple[List["List[str]"], ...]]',
])
def test_complex_annotations(
    assert_errors,
    parse_ast_tree,
    template,
    code,
    mode,
    default_options,
):
    """Testing that expressions with correct call chain length work well."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = AnnotationComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooComplexAnnotationViolation])


@pytest.mark.parametrize('template', [
    annassign_template,
    function_arg_template,
    function_return_template,
    class_field_template,
])
@pytest.mark.parametrize('code', [
    'List[List[int]]',
    '"List[List[int]]"',
    'List["List[int]"]',
])
def test_complex_annotations_config(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    template,
    code,
    mode,
    options,
):
    """Testing that expressions with correct call chain length work well."""
    tree = parse_ast_tree(mode(template.format(code)))

    option_values = options(max_annotation_complexity=2)
    visitor = AnnotationComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooComplexAnnotationViolation])
    assert_error_text(visitor, '3', option_values.max_annotation_complexity)
