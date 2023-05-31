"""
Integration test that our linter does not break on different random programs.

We generate thousands of them with the help of ``hypothesis`` and ensure
that they are parsed and processed correctly.

We cannot tell whether or not violations are correctly shown by a random input,
but we can tell that our program did not raise any exceptions at least.

See also:
    https://github.com/HypothesisWorks/hypothesis
    https://github.com/Zac-HD/hypothesmith

"""

import io
import tokenize

import hypothesmith
from hypothesis import HealthCheck, given, reject, settings

from wemake_python_styleguide.checker import Checker

settings.register_profile(
    'slow', deadline=None, suppress_health_check=list(HealthCheck),
)
settings.load_profile('slow')


def _fixup(string: str) -> str:
    """Avoid known issues with tokenize() by editing the string."""
    return ''.join(
        char
        for char in string
        if char.isprintable()
    ).strip().strip('\\').strip() + '\n'


@given(source_code=hypothesmith.from_grammar().map(_fixup))
@settings(print_blob=True)
def test_no_exceptions(
    source_code,
    default_options,
    parse_ast_tree,
):
    """
    This testcase is a complex example of magic.

    We use property based-test to generate python programs for us.
    And then we ensure that our linter does not crash on arbitrary input.
    """
    try:
        tree = parse_ast_tree(str(source_code.encode('utf-8-sig')))
    except (UnicodeEncodeError, SyntaxError):
        reject()
        raise

    lines = io.StringIO(source_code)
    tokens = list(tokenize.generate_tokens(lambda: next(lines)))

    Checker.parse_options(default_options)
    checker = Checker(tree, tokens)

    for violation in checker.run():
        assert isinstance(violation[0], int)
        assert isinstance(violation[1], int)
        assert violation[2].startswith('WPS'), violation[2]
        assert 'WPS0' not in violation[2]
        assert violation[3] == Checker
