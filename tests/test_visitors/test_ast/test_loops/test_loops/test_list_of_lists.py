import pytest

from wemake_python_styleguide.visitors.ast.loops import WrongLoopDefinitionVisitor

code_that_breaks = """
[ l for l in
  ([x] for x in (1, 2, 3))
]
"""

code_that_works = """
[ l for l in
  [x for x in (1, 2, 3)]
]
"""

code_with_complex_loop = """
[ l for l in
  ([x] for x in (1, 2, 3) if x > 1)
]
"""

@pytest.mark.parametrize('code', [
    code_that_breaks,
    code_that_works,
    code_with_complex_loop,
])
def test_loop_definition(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Test the false positive scenario where WPS335 warning is triggered."""
    tree = parse_ast_tree(code)

    visitor = WrongLoopDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
    assert_error_text(visitor, [], None)
