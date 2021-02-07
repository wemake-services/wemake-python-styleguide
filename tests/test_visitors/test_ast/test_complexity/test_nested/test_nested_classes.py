import pytest

from wemake_python_styleguide.options.defaults import NESTED_CLASSES_WHITELIST
from wemake_python_styleguide.violations.best_practices import (
    NestedClassViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NestedComplexityVisitor,
)

nested_class_in_class = """
class Parent(object):
    class {0}(object): ...
"""

nested_class_in_method = """
class Parent(object):
    def container(self):
        class {0}(object): ...
"""

nested_class_in_function = """
def container():
    class {0}(object): ...
"""

nested_class_in_if = """
def container():
    if some_value:
        class {0}(object): ...
"""

nested_class_in_if_else = """
def container():
    if some_value:
        ...
    else:
        class {0}(object): ...
"""

nested_class_in_context_manager = """
def container():
    with open() as file_obj:
        class {0}(object): ...
"""

nested_class_in_for_loop = """
def container():
    for some in iterable():
        class {0}(object): ...
"""

nested_class_in_while_loop = """
def container():
    while True:
        class {0}(object): ...
"""

nested_class_in_try = """
def container():
    try:
        class {0}(object): ...
    except:
        ...
"""

nested_class_in_except = """
def container():
    try:
        ...
    except:
        class {0}(object): ...
"""

nested_class_in_try_else = """
def container():
    try:
        ...
    except:
        ...
    else:
        class {0}(object): ...
"""

nested_class_in_try_finally = """
def container():
    try:
        ...
    finally:
        class {0}(object): ...
"""


@pytest.mark.parametrize('code', [
    nested_class_in_class,
    nested_class_in_method,
    nested_class_in_function,
    nested_class_in_if,
    nested_class_in_if_else,
    nested_class_in_context_manager,
    nested_class_in_for_loop,
    nested_class_in_while_loop,
    nested_class_in_try,
    nested_class_in_except,
    nested_class_in_try_else,
    nested_class_in_try_finally,
])
def test_nested_class(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that nested classes are restricted."""
    nested_name = 'NestedClass'
    tree = parse_ast_tree(mode(code.format(nested_name)))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedClassViolation])
    assert_error_text(visitor, nested_name)


@pytest.mark.parametrize('whitelist_name', NESTED_CLASSES_WHITELIST)
@pytest.mark.parametrize('code', [
    nested_class_in_class,
])
def test_whitelist_nested_classes(
    assert_errors,
    parse_ast_tree,
    whitelist_name,
    code,
    default_options,
    mode,
):
    """Testing that it is possible to nest whitelisted classes."""
    tree = parse_ast_tree(mode(code.format(whitelist_name)))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('whitelist_name', [
    *NESTED_CLASSES_WHITELIST,
    'NestedClass',
])
@pytest.mark.parametrize('code', [
    nested_class_in_class,
])
def test_custom_whitelist_nested_classes(
    assert_errors,
    parse_ast_tree,
    whitelist_name,
    code,
    options,
    mode,
):
    """Testing that it is possible to nest custom whitelisted classes."""
    tree = parse_ast_tree(mode(code.format(whitelist_name)))

    option_values = options(
        nested_classes_whitelist=[*NESTED_CLASSES_WHITELIST, 'NestedClass'],
    )

    visitor = NestedComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('whitelist_name', [
    *NESTED_CLASSES_WHITELIST,
    'NestedClass',
])
@pytest.mark.parametrize('code', [
    nested_class_in_method,
    nested_class_in_function,
    nested_class_in_if,
    nested_class_in_if_else,
    nested_class_in_context_manager,
    nested_class_in_for_loop,
    nested_class_in_while_loop,
    nested_class_in_try,
    nested_class_in_except,
    nested_class_in_try_else,
    nested_class_in_try_finally,
])
def test_whitelist_nested_classes_in_functions(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    whitelist_name,
    code,
    default_options,
    mode,
):
    """Testing that it is restricted to nest any classes in functions."""
    tree = parse_ast_tree(mode(code.format(whitelist_name)))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedClassViolation])
    assert_error_text(visitor, whitelist_name)


def test_ordinary_class(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that it is possible to write basic classes."""
    code = """
    class Ordinary(object):
        def method(self): ...

    class Second(Ordinary):
        def method(self): ...
    """
    tree = parse_ast_tree(mode(code))

    visitor = NestedComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
