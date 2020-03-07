import pytest

from wemake_python_styleguide.violations.best_practices import (
    TryExceptMultipleReturnPathViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UselessExceptCaseViolation,
)
from wemake_python_styleguide.visitors.ast.exceptions import (
    WrongTryExceptVisitor,
)

# Correct:

right_outside1 = """
def function():  # we need function to use ``return``
    for _ in range(10):
        try:
            ...
        except:
            {0}
        {0}
"""

right_outside2 = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            ...
        {0}
"""

right_try_except = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
"""

right_try_except_multiple = """
def function():
    for _ in range(10):
        try:
            {0}
        except FirstError:
            {0}
        except SecondError:
            {0}
"""

right_except_else = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            {0}
        else:
            {0}
"""

right_multiple_except_else = """
def function():
    for _ in range(10):
        try:
            ...
        except FirstError:
            {0}
        except SecondError:
            {0}
        else:
            {0}
"""

right_else = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            ...
        else:
            {0}
"""

right_try_except_and_else = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        else:
            ...
"""

right_finally = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            ...
        finally:
            {0}
"""

right_try_catch_and_finally = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        finally:
            ...
"""

right_try_catch_and_else_and_finally1 = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        else:
            ...
        finally:
            ...
"""

right_try_catch_and_else_and_finally2 = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            ...
        else:
            ...
        finally:
            {0}
"""

right_try_catch_and_else_and_finally3 = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            {0}
        else:
            {0}
        finally:
            ...
"""

right_try_catch_and_else_and_finally4 = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            ...
        else:
            ...
        finally:
            ...
"""

# Wrong:

wrong_try_finally = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            ...
        finally:
            {0}
"""

wrong_except_finally = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            {0}
        finally:
            {0}
"""

wrong_multiple_except_finally1 = """
def function():
    for _ in range(10):
        try:
            ...
        except FirstError:
            {0}
        except SecondError:
            ...
        finally:
            {0}
"""

wrong_multiple_except_finally2 = """
def function():
    for _ in range(10):
        try:
            ...
        except FirstError:
            ...
        except SecondError:
            {0}
        finally:
            {0}
"""

wrong_multiple_except_finally3 = """
def function():
    for _ in range(10):
        try:
            ...
        except FirstError:
            {0}
        except SecondError:
            {0}
        finally:
            {0}
"""

wrong_else_finally = """
def function():
    for _ in range(10):
        try:
            ...
        except:
            ...
        else:
            {0}
        finally:
            {0}
"""

wrong_try_finally = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        finally:
            {0}
"""

wrong_try_else = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            ...
        else:
            {0}
"""

wrong_try_except_else = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        else:
            {0}
"""

wrong_all = """
def function():
    for _ in range(10):
        try:
            {0}
        except:
            {0}
        else:
            {0}
        finally:
            {0}
"""

wrong_all2 = """
def function():
    for _ in range(10):
        try:
            {0}
        except FirstError:
            {0}
        except SecondError:
            {0}
        else:
            {0}
        finally:
            {0}
"""

wrong_all3 = """
def function():
    for _ in range(10):
        try:
            {0}
        except FirstError:
            ...
        except SecondError:
            {0}
        else:
            {0}
        finally:
            {0}
"""

wrong_all4 = """
def function():
    for _ in range(10):
        try:
            {0}
        except FirstError:
            {0}
        except SecondError:
            ...
        else:
            {0}
        finally:
            {0}
"""

# All statements in once:

all_nodes = """
def function():
    for _ in range(10):
        try:
            {0}
        except FirstError:
            {1}
        except SecondError:
            {2}
        else:
            {3}
        finally:
            {4}
"""


@pytest.mark.parametrize('statement', [
    'return',
    'return None',
    'return 1',
    'raise ValueError',
    'raise ValueError()',
    'raise TypeError(1)',
])
@pytest.mark.parametrize('code', [
    wrong_try_finally,
    wrong_except_finally,
    wrong_multiple_except_finally1,
    wrong_multiple_except_finally2,
    wrong_multiple_except_finally3,
    wrong_else_finally,
    wrong_try_finally,
    wrong_try_else,
    wrong_try_except_else,
    wrong_all,
    wrong_all2,
    wrong_all3,
    wrong_all4,
])
def test_wrong_return_in_else_or_finally(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Violations are raised when there are multiple return path."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [TryExceptMultipleReturnPathViolation],
        (UselessExceptCaseViolation),
    )


@pytest.mark.parametrize('statement', [
    'return',
    'return None',
    'return 1',
    'raise ValueError',
    'raise ValueError()',
    'raise TypeError(1)',
])
@pytest.mark.parametrize('code', [
    right_outside1,
    right_outside2,
    right_try_except,
    right_try_except_multiple,
    right_except_else,
    right_multiple_except_else,
    right_else,
    right_try_except_and_else,
    right_finally,
    right_try_catch_and_finally,
    right_try_catch_and_else_and_finally1,
    right_try_catch_and_else_and_finally2,
    right_try_catch_and_else_and_finally3,
    right_try_catch_and_else_and_finally4,
])
def test_correct_return_path_in_try_except(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
    mode,
):
    """Violations are not raised when return path is correct."""
    tree = parse_ast_tree(mode(code.format(statement)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], (UselessExceptCaseViolation))


@pytest.mark.parametrize('statements', [
    # try, except1, except2, else, finally
    ('break', '...', '...', 'raise ValueError', '...'),
    ('break', '...', '...', 'return', '...'),
    ('return', '...', '...', 'break', '...'),
    ('return 0', '...', '...', 'raise ValueError', '...'),
    ('raise ValueError(1)', '...', '...', 'return 1', '...'),
    ('raise ValueError(1)', '...', '...', 'break', '...'),

    ('...', '...', '...', 'raise ValueError', 'return 0'),
    ('...', '...', '...', 'raise ValueError', 'return None'),
    ('...', '...', '...', 'break', 'return'),
    ('...', '...', '...', 'break', 'raise ValueError'),
    ('...', '...', '...', 'return', 'return 1'),
    ('...', '...', '...', 'return', 'raise ValueError()'),

    ('break', '...', '...', '...', 'raise ValueError'),
    ('break', '...', '...', '...', 'return'),
    ('return', '...', '...', '...', 'raise ValueError(1)'),
    ('return 0', '...', '...', '...', 'raise ValueError'),
    ('raise ValueError(1)', '...', '...', '...', 'return 1'),
    ('raise ValueError(1)', '...', '...', '...', 'return'),

    ('...', 'break', '...', '...', 'raise ValueError'),
    ('...', 'break', '...', '...', 'return'),
    ('...', 'return', '...', '...', 'raise ValueError(1)'),
    ('...', 'return 0', '...', '...', 'raise ValueError'),
    ('...', 'raise ValueError(1)', '...', '...', 'return 1'),
    ('...', 'raise ValueError(1)', '...', '...', 'return 0'),

    ('...', '...', 'break', '...', 'raise ValueError'),
    ('...', '...', 'break', '...', 'return'),
    ('...', '...', 'return', '...', 'raise ValueError'),
    ('...', '...', 'return 0', '...', 'raise ValueError'),
    ('...', '...', 'raise ValueError(1)', '...', 'return 1'),
    ('...', '...', 'raise ValueError(1)', '...', 'return 0'),
])
def test_different_nodes_trigger_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
    statements,
):
    """Violations are raised when there are multiple return path."""
    tree = parse_ast_tree(mode(all_nodes.format(*statements)))

    visitor = WrongTryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TryExceptMultipleReturnPathViolation])
