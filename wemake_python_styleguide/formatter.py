"""
Our very own ``flake8`` formatter for better error messages.

That's how all ``flake8`` formatters work:

.. mermaid::
   :caption: ``flake8`` formatting API calls order.

    graph LR
        F2[start]  --> F3[after_init]
        F3         --> F4[start]
        F4         --> F5[beginning]
        F5         --> F6[handle]
        F6         --> F7[format]
        F6	       --> F8[show_source]
        F6	       --> F9[show_statistic]
        F7         --> F10[finished]
        F8         --> F10[finished]
        F9         --> F10[finished]
        F10       -.-> F5
        F10        --> F11[stop]

.. autoclass:: WemakeFormatter
   :no-undoc-members:

"""

from collections import defaultdict
from typing import ClassVar, DefaultDict, List

from flake8.formatting.base import BaseFormatter
from flake8.statistics import Statistics
from flake8.style_guide import Violation
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer
from typing_extensions import Final

from wemake_python_styleguide.version import pkg_version

#: That url is generated and hosted by Sphinx.
DOCS_URL_TEMPLATE: Final = (
    'https://wemake-python-stylegui.de/en/{0}/pages/usage/violations/'
)


class WemakeFormatter(BaseFormatter):  # noqa: WPS214
    """
    We need to format our style :term:`violations <violation>` beatifully.

    The default formatter does not allow us to do that.
    What things do we miss?

    1. Spacing, everything is just mixed up and glued together
    2. Colors and decoration, some information is easier
       to gather just with colors or underlined text
    3. Grouping, we need explicit grouping by filename
    4. Incomplete and non-informative statistics

    """

    _doc_url: ClassVar[str] = DOCS_URL_TEMPLATE.format(pkg_version)

    # API:

    def after_init(self):
        """Called after the original ``init`` is used to set extra fields."""
        self._lexer = PythonLexer()
        self._formatter = TerminalFormatter()

        # Logic:
        self._proccessed_filenames: List[str] = []
        self._error_count = 0

    def handle(self, error: Violation) -> None:  # noqa: WPS110
        """Processes each :term:`violation` to print it and all related."""
        if error.filename not in self._proccessed_filenames:
            self._print_header(error.filename)
            self._proccessed_filenames.append(error.filename)

        super().handle(error)
        self._error_count += 1

    def format(self, error: Violation) -> str:  # noqa: WPS125
        """Called to format each individual :term:`violation`."""
        return '{newline}  {row_col:<8} {code:<5} {text}'.format(
            newline=self.newline if self._should_show_source(error) else '',
            code=error.code,
            text=error.text,
            row_col='{0}:{1}'.format(error.line_number, error.column_number),
        )

    def show_source(self, error: Violation) -> str:
        """Called when ``--show-source`` option is provided."""
        if not self._should_show_source(error):
            return ''

        formated_line = error.physical_line.lstrip()
        adjust = len(error.physical_line) - len(formated_line)

        code = _highlight(
            formated_line,
            self._lexer,
            self._formatter,
        )

        return '  {code}  {pointer}^'.format(
            code=code,
            pointer=' ' * (error.column_number - 1 - adjust),
        )

    def show_statistics(self, statistics: Statistics) -> None:  # noqa: WPS210
        """Called when ``--statistic`` option is passed."""
        all_errors = 0
        for error_code in statistics.error_codes():
            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)

            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            all_errors += count
            error_by_file = _count_per_filename(statistics, error_code)

            self._print_violation_per_file(
                statistic,
                error_code,
                count,
                error_by_file,
            )

        self._write(self.newline)
        self._write(_underline(_bold('All errors: {0}'.format(all_errors))))

    def stop(self) -> None:
        """Runs once per app when the formatting ends."""
        if self._error_count:
            message = '{0}Full list of violations and explanations:{0}{1}'
            self._write(message.format(self.newline, self._doc_url))

    # Our own methods:

    def _print_header(self, filename: str) -> None:
        self._write(
            '{newline}{filename}'.format(
                filename=_underline(_bold(filename)),
                newline=self.newline,
            ),
        )

    def _print_violation_per_file(
        self,
        statistic: Statistics,
        error_code: str,
        count: int,
        error_by_file: DefaultDict[str, int],
    ):
        self._write(
            '{newline}{error_code}: {message}'.format(
                newline=self.newline,
                error_code=_bold(error_code),
                message=statistic.message,
            ),
        )
        for filename, error_count in error_by_file.items():
            self._write(
                '  {error_count:<5} {filename}'.format(
                    error_count=error_count,
                    filename=filename,
                ),
            )
        self._write(_underline('Total: {0}'.format(count)))

    def _should_show_source(self, error: Violation) -> bool:
        return self.options.show_source and error.physical_line is not None


# Formatting text:

def _bold(text: str) -> str:
    r"""
    Returns bold formatted text.

    >>> _bold('Hello!')
    '\x1b[1mHello!\x1b[0m'

    """
    return '\033[1m{0}\033[0m'.format(text)


def _underline(text: str) -> str:
    r"""
    Returns underlined formatted text.

    >>> _underline('Hello!')
    '\x1b[4mHello!\x1b[0m'

    """
    return '\033[4m{0}\033[0m'.format(text)


def _highlight(source: str, lexer, formatter) -> str:
    """
    Highlights source code. Might fail.

    See also:
        https://github.com/wemake-services/wemake-python-styleguide/issues/794

    """
    try:
        return highlight(source, lexer, formatter)
    except Exception:  # pragma: no cover
        # Might fail on some systems, when colors are set incorrectly,
        # or not available at all. In this case code will be just text.
        return source


# Helpers:

def _count_per_filename(
    statistics: Statistics,
    error_code: str,
) -> DefaultDict[str, int]:
    filenames: DefaultDict[str, int] = defaultdict(int)
    stats_for_error_code = statistics.statistics_for(error_code)

    for stat in stats_for_error_code:
        filenames[stat.filename] += stat.count

    return filenames
