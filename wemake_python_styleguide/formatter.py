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

import os
from collections import defaultdict
from typing import ClassVar, Final

from flake8.formatting.base import BaseFormatter
from flake8.statistics import Statistic, Statistics
from flake8.violation import Violation
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer

from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE
from wemake_python_styleguide.version import pkg_version

#: That url is generated and hosted by Sphinx.
_DOCS_URL_TEMPLATE: Final = (
    'https://wemake-python-styleguide.rtfd.io/en/{0}/pages/usage/violations/'
)

#: Option to disable any code highlight and text output format.
#: See https://no-color.org
_NO_COLOR: Final = os.environ.get('NO_COLOR', '0') == '1'


class WemakeFormatter(BaseFormatter):  # noqa: WPS214
    """
    We need to format our style :term:`violations <violation>` beautifully.

    The default formatter does not allow us to do that.
    What things do we miss?

    1. Spacing, everything is just mixed up and glued together
    2. Colors and decoration, some information is easier
       to gather just with colors or underlined text
    3. Grouping, we need explicit grouping by filename
    4. Incomplete and non-informative statistics

    """

    _doc_url: ClassVar[str] = _DOCS_URL_TEMPLATE.format(pkg_version)

    # API:

    def after_init(self) -> None:
        """Called after the original ``init`` is used to set extra fields."""
        self._lexer = PythonLexer()
        self._formatter = TerminalFormatter()

        # Logic:
        self._processed_filenames: list[str] = []
        self._error_count = 0

    def handle(self, error: Violation) -> None:  # noqa: WPS110
        """Processes each :term:`violation` to print it and all related."""
        if error.filename not in self._processed_filenames:
            self._print_header(error.filename)
            self._processed_filenames.append(error.filename)

        line = self.format(error)
        source = self.show_source(error)
        link = self._show_link(error)

        self._write(line)
        if link:
            self._write(link)
        if source:
            self._write(source)

        self._error_count += 1

    def format(self, error: Violation) -> str:  # noqa: WPS125
        """Called to format each individual :term:`violation`."""
        return '{newline}  {row_col:<8} {code:<5} {text}'.format(
            newline=self.newline if self._should_show_source(error) else '',
            code=error.code,
            text=error.text,
            row_col=f'{error.line_number}:{error.column_number}',
        )

    def show_source(self, error: Violation) -> str:
        """Called when ``--show-source`` option is provided."""
        if not self._should_show_source(error) or not error.physical_line:
            return ''

        formatted_line = error.physical_line.lstrip()
        adjust = len(error.physical_line) - len(formatted_line)

        code = _highlight(
            formatted_line,
            self._lexer,
            self._formatter,
        )

        return '  {code}  {spacing}^'.format(
            code=code,
            spacing=' ' * (error.column_number - 1 - adjust),
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
        self._write(_underline(_bold(f'All errors: {all_errors}')))

    def stop(self) -> None:
        """Runs once per app when the formatting ends."""
        if self._error_count:
            message = '{0}Full list of violations and explanations:{0}{1}'
            self._write(message.format(self.newline, self._doc_url))

    # Our own methods:

    def _show_link(self, error: Violation) -> str:
        """Called when ``--show-violation-links`` option is provided."""
        if not self.options.show_violation_links:
            return ''

        return '  {spacing}-> {link}'.format(
            spacing=' ' * 9,
            link=SHORTLINK_TEMPLATE.format(error.code),
        )

    def _print_header(self, filename: str) -> None:
        header = _underline(_bold(os.path.normpath(filename)))
        self._write(f'{self.newline}{header}')

    def _print_violation_per_file(
        self,
        statistic: Statistic,
        error_code: str,
        count: int,
        error_by_file: defaultdict[str, int],
    ) -> None:
        bold_code = _bold(error_code)
        self._write(
            f'{self.newline}{bold_code}: {statistic.message}',
        )
        for filename, error_count in error_by_file.items():
            self._write(
                f'  {error_count:<5} {filename}',
            )
        self._write(_underline(f'Total: {count}'))

    def _should_show_source(self, error: Violation) -> bool:
        return self.options.show_source and error.physical_line is not None


# Formatting text:


def _bold(text: str, *, no_color: bool = _NO_COLOR) -> str:
    r"""
    Returns bold formatted text.

    >>> _bold('Hello!')
    '\x1b[1mHello!\x1b[0m'

    Returns non-formatted text if environment variable ``NO_COLOR=1``.

    >>> _bold('Hello!', no_color=True)
    'Hello!'

    """
    if no_color:
        return text
    return f'\033[1m{text}\033[0m'


def _underline(text: str, *, no_color: bool = _NO_COLOR) -> str:
    r"""
    Returns underlined formatted text.

    >>> _underline('Hello!')
    '\x1b[4mHello!\x1b[0m'

    Returns non-formatted text if environment variable ``NO_COLOR=1``.

    >>> _underline('Hello!', no_color=True)
    'Hello!'

    """
    if no_color:
        return text
    return f'\033[4m{text}\033[0m'


def _highlight(
    source: str,
    lexer: PythonLexer,
    formatter: TerminalFormatter,
    *,
    no_color: bool = _NO_COLOR,
) -> str:
    """
    Highlights source code. Might fail.

    Returns non-formatted text if environment variable ``NO_COLOR=1``.

    See also:
        https://github.com/wemake-services/wemake-python-styleguide/issues/794
        https://no-color.org

    """
    if no_color:
        return source
    try:
        return highlight(  # type: ignore[no-any-return]
            source,
            lexer,
            formatter,
        )
    except Exception:  # pragma: no cover
        # Might fail on some systems, when colors are set incorrectly,
        # or not available at all. In this case code will be just text.
        return source


# Helpers:


def _count_per_filename(
    statistics: Statistics,
    error_code: str,
) -> defaultdict[str, int]:
    filenames: defaultdict[str, int] = defaultdict(int)
    stats_for_error_code = statistics.statistics_for(error_code)

    for stat in stats_for_error_code:
        filenames[stat.filename] += stat.count

    return filenames
