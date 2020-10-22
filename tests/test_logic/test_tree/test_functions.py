import pytest

from wemake_python_styleguide.logic.tree import functions


@pytest.mark.parametrize(('function_call', 'function_name'), [
    # Simple builtin functions
    ('print("Hello world!")', 'print'),
    ('int("10")', 'int'),
    ('bool(1)', 'bool'),
    ('open("/tmp/file.txt", "r")', 'open'),
    ('str(10)', 'str'),

    # Functions in modules
    ('datetime.timedelta(days=1)', 'datetime.timedelta'),
    ('cmath.sqrt(100)', 'cmath.sqrt'),

    # Functions in (made up) objects
    ('dt.strftime("%H:%M")', 'dt.strftime'),
    ('obj.funct()', 'obj.funct'),
])
def test_given_function_called_no_split(
    parse_ast_tree, function_call: str, function_name: str,
) -> None:
    """Test given_function_called without splitting the modules."""
    tree = parse_ast_tree(function_call)
    node = tree.body[0].value
    called_function = functions.given_function_called(node, [function_name])
    assert called_function == function_name


@pytest.mark.parametrize(('function_call', 'function_name'), [
    # Simple builtin functions
    ('print("Hello world!")', 'print'),
    ('int("10")', 'int'),
    ('bool(1)', 'bool'),
    ('open("/tmp/file.txt", "r")', 'open'),
    ('str(10)', 'str'),

    # Functions in modules
    ('datetime.timedelta(days=1)', 'timedelta'),
    ('cmath.sqrt(100)', 'sqrt'),

    # Functions in (made up) objects
    ('dt.strftime("%H:%M")', 'strftime'),
    ('obj.funct()', 'funct'),
])
def test_given_function_called_with_split(
    parse_ast_tree, function_call: str, function_name: str,
) -> None:
    """Test given_function_called splitting the modules."""
    tree = parse_ast_tree(function_call)
    node = tree.body[0].value
    called_function = functions.given_function_called(
        node,
        [function_name],
        split_modules=True,
    )
    assert called_function == function_name
