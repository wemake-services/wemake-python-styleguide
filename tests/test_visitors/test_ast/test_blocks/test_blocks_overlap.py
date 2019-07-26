# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

import_and_class1 = """
import overlap

class overlap: ...
"""

import_and_class2 = """
class overlap: ...

import overlap
"""

import_and_function1 = """
import overlap

def overlap(): ...
"""

import_and_function2 = """
def overlap(): ...

import overlap
"""

import_and_try = """
import overlap

try:
    ...
except Exception as overlap:
    ...
"""

loop_and_with = """
def context():
    for overlap in some():
        ...

    with open() as overlap:
        ...
"""


@pytest.mark.parametrize('code', [
    import_and_class1,
    import_and_class2,
    import_and_function1,
    import_and_function2,
    import_and_try,
    loop_and_with,
])
def test_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that overlaps between blocks are forbiden.."""
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, 'overlap')
