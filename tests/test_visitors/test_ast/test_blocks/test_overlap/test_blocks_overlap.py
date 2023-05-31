import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Wrong:

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

loop_and_loop1 = """
def context():
    for overlap in some():
        ...

    for overlap in other():
        ...
"""

loop_and_loop2 = """
def context():
    for overlap, attr.wrong in some():
        ...

    for other.wrong, overlap in other():
        ...
"""

import_and_walrus = """
import overlap

if overlap := other():
    ...
"""

# Correct:

unused_variables_overlap1 = """
def context():
    for first, _ in some():
        ...

    for _, second in other():
        ...
"""

unused_variables_overlap2 = """
def context():
    for first, __ in some():
        ...

    for __, second in other():
        ...
"""

unused_variables_overlap3 = """
def context():
    for first.wrong, __ in some():
        ...

    for __, second.wrong in other():
        ...
"""

annotation_overlap = """
def context():
    conn: Connection
    with db.get_conn() as conn:
        ...
"""


@pytest.mark.parametrize('code', [
    import_and_class1,
    import_and_class2,
    import_and_function1,
    import_and_function2,
    import_and_try,
    loop_and_with,
    loop_and_loop1,
    loop_and_loop2,
    import_and_walrus,
])
def test_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that overlaps between blocks are forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, 'overlap')


@pytest.mark.parametrize('code', [
    unused_variables_overlap1,
    unused_variables_overlap2,
    unused_variables_overlap3,
    annotation_overlap,
])
def test_block_correct_overlap(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that correct overlaps are ok."""
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
