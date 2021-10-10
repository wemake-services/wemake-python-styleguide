from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionSubclassViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassDefVisitor

class_with_base = """
class Meta({0}):
    '''Docs.'''
"""


def test_base_exception_subclass(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that it is not possible to subclass `BaseException`."""
    tree = parse_ast_tree(class_with_base.format('BaseException'))

    visitor = WrongClassDefVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BaseExceptionSubclassViolation])
