
import pytest

from wemake_python_styleguide.violations.naming import ProtectedNameViolation
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor

correct_import = "from requests.api import post"
protected_module = "from security.library import _protected"
protected_path = "from path._protected.somewhat import test"


@pytest.mark.parametrize('code', [
    correct_import,
])
def test_correct_import(assert_errors, parse_ast_tree, code, default_options):
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    protected_module,
    protected_path
])
def test_incorrect_import(assert_errors, parse_ast_tree, code, default_options):
    tree = parse_ast_tree(code)
    visitor = WrongImportVisitor(default_options, tree=tree)
    visitor.run()
    assert_errors(visitor, [ProtectedNameViolation])
