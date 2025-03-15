import pytest

from wemake_python_styleguide.compat.constants import PY313

if not PY313:  # pragma: >=3.13 no cover
    pytest.skip(  # pragma: no cover
        reason='Defaulting type params were added in python 3.13+',
        allow_module_level=True,
    )

from wemake_python_styleguide.violations.best_practices import (
    SneakyTypeVarWithDefaultViolation,
)
from wemake_python_styleguide.visitors.ast.classes.classdef import (
    ConsecutiveDefaultTypeVarsVisitor,
)

class_header_formats = ['Class[{0}]', 'Class(Generic[{0}])']
various_code = (
    'pi = 3.14\n'
    'a = obj.method_call()\n'
    'w, h = get_size()\n'
    'obj.field = function_call()\n'
    'AlmostTypeVar = NotReallyATypeVar()\n'
    "NonDefault = TypeVar('NonDefault')\n"
)
classes_with_various_bases = (
    'class SimpleBase(object): ...\n'
    'class NotANameSubscript(Some.Class[object]): ...\n'
    'class NotAGenericBase(NotAGeneric[T]): ...\n'
    'class OldGenericDefinition(Generic[T]): ...\n'
)


def test_sneaky_type_var_with_default(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that WPS477 works correctly."""
    src = 'class Class[T=int, *Ts=*tuple[int, ...]]: ...'

    tree = parse_ast_tree(src)

    visitor = ConsecutiveDefaultTypeVarsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [SneakyTypeVarWithDefaultViolation])


correct_typevar_and_tuple = """
T = TypeVar('T')
Ts = TypeVarTuple('Ts')
class Class(Generic[T, *Ts]): ...
"""
correct_default_typevar_and_tuple = """
T = TypeVar('T', default=int)
Ts = TypeVarTuple('Ts')
class Class(Generic[T, *Ts]): ...
"""
correct_new_typevar_and_tuple = 'class Class[T, *Ts]: ...'


@pytest.mark.parametrize(
    'src',
    [
        correct_typevar_and_tuple,
        correct_default_typevar_and_tuple,
        correct_new_typevar_and_tuple,
    ],
)
def test_type_var_ignored(
    assert_errors,
    parse_ast_tree,
    default_options,
    src,
):
    """Test that WPS477 ignores non-defaulted and old TypeVars."""
    tree = parse_ast_tree(src)

    visitor = ConsecutiveDefaultTypeVarsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_usual_code_ignored(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Test that WPS477 ignores unrelated classdefs."""
    tree = parse_ast_tree(classes_with_various_bases)

    visitor = ConsecutiveDefaultTypeVarsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
