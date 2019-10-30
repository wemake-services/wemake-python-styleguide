# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    StatementHasNoEffectViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    MisrefactoredAssignmentViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)

# Modules:

module_template = """
{0}
"""

# Simple conditions:

if_template = """
if some:
    {0}
"""

if_elif_template = """
if some:
    print()
elif not some:
    {0}
"""

if_else_template = """
if some:
    print()
else:
    {0}
"""

# Loops:

for_template = """
for some in []:
    {0}
"""

for_else_template = """
for some in []:
    print()
else:
    {0}
"""

while_template = """
while True:
    {0}
"""

while_else_template = """
while True:
    print()
else:
    {0}
"""

# Exception handling:

try_template = """
try:
    {0}
except Exception:
    print()
"""

try_except_template = """
try:
    print()
except Exception:
    {0}
"""

try_else_template = """
try:
    print()
except Exception:
    print()
else:
    {0}
"""

try_finally_template = """
try:
    print()
finally:
    {0}
"""

# Context managers:

with_template = """
with some:
    {0}
"""

# Functions:

function_template = """
def function():
    {0}
"""

# Classes:

class_template = """
class Test(object):
    {0}
"""

# Async:

async_function_template = """
async def function():
    {0}
"""

async_with_template = """
async def container():
    async with some:
        {0}
"""

async_for_template = """
async def container():
    async for some in []:
        {0}
"""

async_for_else_template = """
async def container():
    async for some in []:
        print()
    else:
        {0}
"""


@pytest.mark.parametrize('code', [
    module_template,

    if_template,
    if_elif_template,
    if_else_template,

    for_template,
    for_else_template,
    while_template,
    while_else_template,

    try_template,
    try_except_template,
    try_else_template,
    try_finally_template,

    with_template,

    function_template,
    class_template,

    async_function_template,
    async_with_template,
    async_for_template,
    async_for_else_template,
])
@pytest.mark.parametrize('statement', [
    'print',
    'object.mro',
    '3 > 4',
    '1 + 2',
    '-100',
])
def test_statement_with_no_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StatementHasNoEffectViolation])


@pytest.mark.parametrize('code', [
    module_template,
])
@pytest.mark.parametrize('statement', [
    'x += x + 2',
    'x -= x - 1',
    'x *= x * 1',
    'x /= x / 1',
    'x **= x ** 1',
    'x ^= x ^ 1',
    'x %= x % 1',
    'x >>= x >> 1',
    'x <<= x << 1',
    'x &= x & 1',
    'x |= x | 1',
])
def test_misrefactored_assignment(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MisrefactoredAssignmentViolation])


@pytest.mark.parametrize('code', [
    module_template,

    if_template,
    if_elif_template,
    if_else_template,

    for_template,
    for_else_template,
    while_template,
    while_else_template,

    try_template,
    try_except_template,
    try_else_template,
    try_finally_template,

    with_template,

    function_template,
    class_template,

    async_function_template,
    async_with_template,
    async_for_template,
    async_for_else_template,
])
@pytest.mark.parametrize('statement', [
    'some_name = 1 + 2',
    'call()',
    'object.mro()',
    'del some',
    'some_var: int',
    'x += 2',
    'x += y + 2',
    'x += check(2)',
    'x -= 1',
    'x *= 1',
    'x **= 1',
    'x /= 1',
    'x ^= 1',
    'x %= 1',
    'x >>= 1',
    'x <<= 1',
    'x &= 1',
    'x |= 1',
    'x -= test(x)',
    'x -= x.attr("a")',
    'x -= test(x)',
    'x -= x.method()',
    'x -= x.attr + 1',
    'x -= test(x) + 1',
    'x = 2 + x',
])
def test_statement_with_regular_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing functions, methods, and assignment works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_template,
])
@pytest.mark.parametrize('statement', [
    'return',
    'yield',
    'yield from some',
    'raise TypeError()',
])
def test_statement_with_function_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that `return` and `yield` works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    async_function_template,
])
@pytest.mark.parametrize('statement', [
    'await some',
    'return',
    'yield',
    'raise TypeError()',
])
def test_statement_with_await_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that `await` works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_template,
    async_function_template,
    class_template,
    module_template,
])
@pytest.mark.parametrize('statement', [
    '"docstring"',
])
def test_statement_with_docstring(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that docstring works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_template,
    if_elif_template,
    if_else_template,

    for_template,
    for_else_template,
    while_template,
    while_else_template,

    try_template,
    try_except_template,
    try_else_template,
    try_finally_template,

    with_template,

    async_with_template,
    async_for_template,
    async_for_else_template,
])
@pytest.mark.parametrize('statement', [
    '"docstring"',
])
def test_statement_with_useless_docstring(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that docstring works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StatementHasNoEffectViolation])
