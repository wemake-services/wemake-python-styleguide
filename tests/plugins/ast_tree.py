import ast
from textwrap import dedent

import pytest

from wemake_python_styleguide.transformations.ast_tree import transform


@pytest.fixture(scope='session')
def parse_ast_tree(compile_code):
    """
    Function to convert code to AST.

    This helper mimics some transformations that generally
    happen in different ``flake8`` plugins that we rely on.

    This list can be extended only when there's a direct need to
    replicate the existing behavior from other plugin.

    It is better to import and reuse the required transformation.
    But in case it is impossible to do, you can reinvent it.

    Order is important.
    """
    def factory(code: str, *, do_compile: bool = True) -> ast.AST:
        code_to_parse = dedent(code)
        if do_compile:
            compile_code(code_to_parse)
        return transform(ast.parse(code_to_parse))
    return factory
