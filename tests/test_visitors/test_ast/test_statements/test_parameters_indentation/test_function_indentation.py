import pytest

from wemake_python_styleguide.visitors.ast.statements import (
    ParametersIndentationViolation,
    WrongParametersIndentationVisitor,
)

# Correct:

correct_single_line_function = 'def test(arg, *args, kw, **kwargs): ...'
correct_multi_line_function = """
def test(
    arg,
    *args,
    kw,
    **kwargs,
): ...
"""

correct_multi_line_function_with_posonly = """
def test(
    arg1,
    /,
    arg2,
    *args,
    kw,
    **kwargs,
): ...
"""

correct_multi_line_function_with_defaults = """
def test(
    arg1,
    arg2=True,
    *args,
    kw1,
    kw2=True,
    **kwargs,
): ...
"""

correct_next_line_function = """
def test(
    arg, *args, kw, **kwargs,
): ...
"""


# Wrong:

wrong_function_indentation1 = """
def test(arg,
         *args, kw, **kwargs): ...
"""

wrong_function_indentation2 = """
def test(arg, *args,
         kw, **kwargs): ...
"""

wrong_function_indentation3 = """
def test(arg, *args, kw,
         **kwargs): ...
"""

wrong_function_indentation4 = """
def test(
    arg, *args,
    kw, **kwargs,
): ...
"""

wrong_function_indentation5 = """
def test(
    arg,
    *args,
    kw, **kwargs,
): ...
"""

wrong_function_indentation6 = """
def test(
    arg, *args,
    kw,
    **kwargs,
): ...
"""

wrong_function_indentation7 = """
def test(
    arg, *args, kw,
    **kwargs,
): ...
"""

wrong_function_indentation8 = """
def test(
    arg1, /,
    arg2, *args, kw, **kwargs,
): ...
"""


@pytest.mark.parametrize('code', [
    correct_single_line_function,
    correct_multi_line_function,
    correct_multi_line_function_with_defaults,
    correct_next_line_function,
    correct_multi_line_function_with_posonly,
])
def test_correct_function_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correctly indented functions work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_function_indentation1,
    wrong_function_indentation2,
    wrong_function_indentation3,
    wrong_function_indentation4,
    wrong_function_indentation5,
    wrong_function_indentation6,
    wrong_function_indentation7,
    wrong_function_indentation8,
])
def test_wrong_function_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that poorly indented functions do not work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ParametersIndentationViolation])
