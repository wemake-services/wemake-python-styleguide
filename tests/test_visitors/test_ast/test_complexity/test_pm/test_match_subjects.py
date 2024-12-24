import pytest

from wemake_python_styleguide.violations.complexity import TooManyMatchSubjectsViolation
from wemake_python_styleguide.visitors.ast.complexity.pm import MatchSubjectsVisitor


match_subjects7 = '''
match some_value:
    case x | y | z:
        pass
    case a | b | c:
        pass
    case d | e | f:
        pass
    case g | h | i:
        pass
    case j | k | l:
        pass
    case m | n | o:
        pass
    case p | q | r:
        pass
'''
match_subjects6 = '''
match some_value:
    case x | y | z:
        pass
    case a | b | c:
        pass
    case d | e | f:
        pass
    case g | h | i:
        pass
    case j | k | l:
        pass
    case m | n | o:
        pass
'''

@pytest.mark.parametrize(
    'code',
    [match_subjects7],
)
def test_match_subjects_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings raise a warning for too many match subjects."""
    tree = parse_ast_tree(code)

    visitor = MatchSubjectsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMatchSubjectsViolation])
    assert_error_text(visitor, '8', baseline=default_options.max_match_subjects)


@pytest.mark.parametrize(
    'code',
    [match_subjects6],
)
def test_match_subjects_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings do not raise a warning for correct match subjects count."""
    tree = parse_ast_tree(code)

    visitor = MatchSubjectsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        match_subjects6,
        match_subjects7,
    ],
)
def test_match_subjects_configured_count(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that settings can reflect the change for match subjects."""
    tree = parse_ast_tree(code)

    option_values = options(max_match_subjects=6)
    visitor = MatchSubjectsVisitor(option_values, tree=tree)
    visitor.run()

    if code == match_subjects7:
        assert_errors(visitor, [TooManyMatchSubjectsViolation])
    else:
        assert_errors(visitor, [])
