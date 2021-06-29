import sys

import astpath
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import PythonLexer

FAIL_CODE = 255

OK_CODE = 0

PATTERN = """
//ClassDef[contains(bases, Name[@id='BaseNodeVisitor'])]/body
/FunctionDef[re:match('visit_.*', @name)
and not(child::body/Expr[last()]/value/Call/func
/Attribute[@attr='generic_visit'])]
"""

# This is needed to stop linter from spewing WPS421 errors.
my_print = print


if __name__ == '__main__':
    if len(sys.argv) == 1:
        my_print('Please provide path to search in!')

    matches = astpath.search(sys.argv[1], PATTERN, print_matches=False)

    if not len(matches):
        exit(OK_CODE)  # noqa: WPS421

    my_print()
    my_print('"self.generic_visit(node)" should be last statement here:')

    for fn, line in matches:
        with open(fn, 'r', encoding='utf-8') as fp:
            source = fp.read()
            lines = source.splitlines()
            highlighted = highlight(
                lines[line - 1],
                PythonLexer(),
                Terminal256Formatter(),
            )
            my_print('\t{0}:{1}\n\t{2}'.format(fn, line, highlighted))

    exit(FAIL_CODE)  # noqa: WPS421
