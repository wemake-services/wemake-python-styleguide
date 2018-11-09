# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    UnreachableCodeViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)

# Modules:

module_template = """
{0}
{1}
"""

# Simple conditions:

if_template = """
if some:
    {0}
    {1}
"""

if_elif_template = """
if some:
    ...
elif not some:
    {0}
    {1}
"""

if_else_template = """
if some:
    ...
else:
    {0}
    {1}
"""

# Loops:

for_template = """
for some in []:
    {0}
    {1}
"""

for_else_template = """
for some in []:
    ...
else:
    {0}
    {1}
"""

while_template = """
while True:
    {0}
    {1}
"""

while_else_template = """
while True:
    ...
else:
    {0}
    {1}
"""

# Exception handling:

try_template = """
try:
    {0}
    {1}
except Exception:
    ...
"""

try_except_template = """
try:
    ...
except Exception:
    {0}
    {1}
"""

try_else_template = """
try:
    ...
except Exception:
    ...
else:
    {0}
    {1}
"""

try_finally_template = """
try:
    ...
finally:
    {0}
    {1}
"""

# Context managers:

with_template = """
with some:
    {0}
    {1}
"""

# Functions:

function_template = """
def function():
    {0}
    {1}
"""

# Classes:

class_template = """
class Test(object):
    {0}
    {1}
"""

# Async:

async_function_template = """
async def function():
    {0}
    {1}
"""

async_with_template = """
async def container():
    async with some:
        {0}
        {1}
"""

async_for_template = """
async def container():
    async for some in []:
        {0}
        {1}
"""

async_for_else_template = """
async def container():
    async for some in []:
        ...
    else:
        {0}
        {1}
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
def test_regular_lines(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing correct order of lines is allowed."""
    tree = parse_ast_tree(code.format('print()', 'raise ValueError()'))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


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
def test_unreachable_code_raise(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format('raise ValueError()', '...'))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnreachableCodeViolation])


@pytest.mark.parametrize('code', [
    function_template,
    async_function_template,
])
def test_unreachable_code_return(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format('return', '...'))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnreachableCodeViolation])


@pytest.mark.parametrize('code', [
    for_template,
    while_template,

    async_for_template,
])
@pytest.mark.parametrize('keyword', [
    'break',
    'continue',
])
def test_unreachable_code_in_loops(
    assert_errors,
    parse_ast_tree,
    code,
    keyword,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format(keyword, '...'))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnreachableCodeViolation])
