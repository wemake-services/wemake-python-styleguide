# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.annotations import (
    UnionNoneViolation,
    WrongAnnotationVisitor,
)

# Correct:

correct_class_union_none_annotation = """
class Test(object):
    arg: Union[int, float, None] = 0.0
"""

correct_class_embedded_union_none_annotation = """
class Test(object):
    arg: Union[Union[int, float, None], float] = 0.0
"""

correct_class_union_annotation = """
class Test(object):
    arg: Union[True, float] = 0.0
"""

correct_class_union_annotation_one_argument = """
class Test(object):
    arg: Union[float] = 0.0
"""

correct_var_union_none_annotation = """
arg: Union[int, float, None] = 0.0
"""

correct_var_embedded_union_none_annotation = """
arg: Union[Union[int, float, None], float] = 0.0
"""

correct_var_union_annotation = """
arg: Union[True, float] = 0.0
"""

correct_var_union_annotation_one_argument = """
arg: Union[float] = 0.0
"""

# Wrong:

wrong_var_union_with_none_annotation = """
arg: Union[int, None] = 0
"""

wrong_embedded_var_union_with_none_annotation = """
arg: Union[Union[int, None], Optional[int]] = 0
"""

wrong_class_union_with_none_annotation = """
class Test(object):
    arg: Union[int, None] = 0
"""

wrong_embedded_class_union_none_annotation = """
class Test(object):
    arg: Union[Union[int, None], Optional[int]] = 0
"""


@pytest.mark.parametrize('code', [
    correct_class_union_none_annotation,
    correct_class_embedded_union_none_annotation,
    correct_class_union_annotation,
    correct_class_union_annotation_one_argument,
    correct_var_union_none_annotation,
    correct_var_embedded_union_none_annotation,
    correct_var_union_annotation,
    correct_var_union_annotation_one_argument,
])
def test_correct_argument_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use correct type annotations."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_var_union_with_none_annotation,
    wrong_embedded_var_union_with_none_annotation,
    wrong_class_union_with_none_annotation,
    wrong_embedded_class_union_none_annotation,
])
def test_wrong_union_none_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect argument annotations is forbiden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnionNoneViolation])
