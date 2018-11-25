# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.statements import (
    ParametersIndentationViolation,
    WrongParametersIndentationVisitor,
)

# Correct:

correct_single_line_tuple = 'xy = (1, 2, 3)'
correct_single_line_list = 'xy = [1, 2, 3]'
correct_single_line_set = 'xy = {1, 2, 3}'
correct_single_line_dict = 'xy = {"key": [1, 2], "other": {1, 2}, "w": (1, 2)}'

correct_multi_line_tuple = """
xy = (
    1,
    2,
    3,
)
"""

correct_multi_line_list = """
xy = [
    1,
    2,
    3,
]
"""

correct_multi_line_set = """
xy = {
    1,
    2,
    3,
}
"""

correct_multi_line_dict = """
xy = {
    1: 1,
    2: 2,
    3: 3,
}
"""

correct_next_line_tuple = """
xy = (
    1, 2, 3,
)
"""

correct_next_line_list = """
xy = [
    1, 2, 3,
]
"""

correct_next_line_set = """
xy = {
    1, 2, 3,
}
"""

correct_next_line_tuple = """
xy = {
    1: 1, 2: 2, 3: 3,
}
"""

correct_nested_collections = """
xy = {
    'key': [
        1, 2, 3,
    ],
    'other': (
        'first',
        'second',
    ),
    'single': {1, 2, 3},
    'multiple': {
        1: [
            1,
            1,
            1,
        ],
    },
    'ending': 5,
}
"""


# Wrong:

wrong_tuple_indentation1 = """
xy = (1,
      2, 3)
"""

wrong_tuple_indentation2 = """
xy = (1, 2,
      3)
"""

wrong_tuple_indentation3 = """
xy = (
    1, 2,
    3,
)
"""

wrong_tuple_indentation4 = """
xy = (
    1,
    2, 3,
)
"""

wrong_list_indentation1 = """
xy = [1,
      2, 3]
"""

wrong_list_indentation2 = """
xy = [1, 2,
      3]
"""

wrong_list_indentation3 = """
xy = [
    1, 2,
    3,
]
"""

wrong_list_indentation4 = """
xy = [
    1,
    2, 3,
]
"""

wrong_set_indentation1 = """
xy = {1,
      2, 3}
"""

wrong_set_indentation2 = """
xy = {1, 2,
      3}
"""

wrong_set_indentation3 = """
xy = {
    1, 2,
    3,
}
"""

wrong_set_indentation4 = """
xy = {
    1,
    2, 3,
}
"""

wrong_dict_indentation1 = """
xy = {1: 1,
      2: 2, 3: 3}
"""

wrong_dict_indentation2 = """
xy = {1: 1, 2: 2,
      3: 3}
"""

wrong_dict_indentation3 = """
xy = {
    1: 1, 2: 2,
    3: 3,
}
"""

wrong_dict_indentation4 = """
xy = {
    1: 1,
    2: 2, 3: 3,
}
"""


@pytest.mark.parametrize('code', [
    correct_single_line_tuple,
    correct_single_line_list,
    correct_single_line_set,
    correct_single_line_dict,
    correct_multi_line_tuple,
    correct_multi_line_list,
    correct_multi_line_set,
    correct_multi_line_dict,
    correct_next_line_tuple,
    correct_next_line_list,
    correct_next_line_set,
    correct_next_line_tuple,
    correct_nested_collections,
])
def test_correct_collection_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correctly indented collections work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_tuple_indentation1,
    wrong_tuple_indentation2,
    wrong_tuple_indentation3,
    wrong_tuple_indentation4,
    wrong_list_indentation1,
    wrong_list_indentation2,
    wrong_list_indentation3,
    wrong_list_indentation4,
    wrong_set_indentation1,
    wrong_set_indentation2,
    wrong_set_indentation3,
    wrong_set_indentation4,
    wrong_dict_indentation1,
    wrong_dict_indentation2,
    wrong_dict_indentation3,
    wrong_dict_indentation4,
])
def test_wrong_collection_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that poorly indented collections do not work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ParametersIndentationViolation])
