import pytest

from wemake_python_styleguide.violations.complexity import (
    CognitiveComplexityViolation,
    CognitiveModuleComplexityViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    CognitiveComplexityVisitor,
)

complex_function = """
def literal_eval(node):
    if isinstance(node, (Constant, NameConstant)):
        return node.value
    elif isinstance(node, (Str, Bytes, Num)):
        # We wrap strings to tell the difference between strings and names:
        return node.n if isinstance(node, Num) else '"{0!r}"'.format(node.s)
    elif isinstance(node, (Tuple, List, Set, Dict)):
        return _convert_iterable(node)
    elif isinstance(node, BinOp) and isinstance(node.op, (Add, Sub)):
        maybe_complex = _convert_complex(node)
        if maybe_complex is not None:
            return maybe_complex
    return _convert_signed_num(node)
"""

# Samples:

function_example = """
def some():
    if condition:
        print('complex')
"""

method_example = """
class Test(object):
    def some():
        if condition:
            print('complex')
"""

empty_module = ''


@pytest.mark.parametrize('code', [
    complex_function,
])
def test_complex_cognitive_function(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that complex cognitive code does not work."""
    tree = parse_ast_tree(mode(code))

    visitor = CognitiveComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [CognitiveComplexityViolation],
        ignored_types=(CognitiveModuleComplexityViolation,),
    )
    assert_error_text(
        visitor, '22', default_options.max_cognitive_score, multiple=True,
    )


@pytest.mark.parametrize('code', [
    function_example,
    method_example,
])
def test_complex_cognitive_options(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Ensures that complex can be modified via settings."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_cognitive_score=0)
    visitor = CognitiveComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [CognitiveComplexityViolation],
        ignored_types=(CognitiveModuleComplexityViolation,),
    )
    assert_error_text(
        visitor, '1', option_values.max_cognitive_score, multiple=True,
    )


@pytest.mark.parametrize('code', [
    function_example,
    method_example,
    empty_module,
])
def test_complex_cognitive_default_options(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that simple cognitive code does work."""
    tree = parse_ast_tree(mode(code))

    visitor = CognitiveComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
