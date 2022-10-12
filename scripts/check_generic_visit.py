import sys
from typing import NoReturn

import astpath
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import PythonLexer
from typing_extensions import Final

FAIL_CODE: Final = 255

OK_CODE: Final = 0

PATTERN: Final = """
//ClassDef[contains(bases, Name[@id='BaseNodeVisitor'])]/body
/FunctionDef[re:match('visit_.*', @name)
and not(child::body/Expr[last()]/value/Call/func/Attribute[@attr='generic_visit'] or
child::body/With[last()]/body/Expr[last()]/value/Call/func/Attribute[@attr='generic_visit'])]
"""  # noqa: E501

# This is needed to stop linter from spewing WPS421 errors.
report = print


def main() -> NoReturn:
    """Check for ``self.generic_visit()`` in all visit methods."""
    if len(sys.argv) == 1:
        report('Please provide path to search in!')

    matches = astpath.search(sys.argv[1], PATTERN, print_matches=False)

    if not len(matches):
        exit(OK_CODE)  # noqa: WPS421

    report()
    report('"self.generic_visit(node)" should be last statement here:')

    for fn, line in matches:
        with open(fn, 'r') as fp:
            lines = fp.read().splitlines()
            report('\t{0}:{1}\n\t{2}'.format(
                fn,
                line,
                highlight(
                    lines[line - 1],
                    PythonLexer(),
                    Terminal256Formatter(),
                )),
            )

    exit(FAIL_CODE)  # noqa: WPS421


if __name__ == '__main__':
    main()
