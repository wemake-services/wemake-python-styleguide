# -*- coding: utf-8 -*-

"""
Custom formatter for ``flake8`` :term:`violations <violation>`.

Tries to be beatiful, compact, and informative.
Improves the default formatter used by ``flake8``.


Usage
-----

To activate this formatter one will need to run:

.. code:: bash

  flake8 --format=wemake your_module.py

Or set the configuration option inside ``setup.cfg`` file:

.. code:: ini

  [flake8]
  format = wemake

Option ``format = wemake`` is included into our default configuration.

To switch back to the default ``flake8`` formatter,
you can use ``format = default`` option.

There are other formatters out there as well.
They can be installed as plugins.


Showing source code
-------------------

You can also (and we recommend to) enable ``--show-source`` option.
It can be passed as a command line argument or set in ``setup.cfg``:

.. code:: ini

  [flake8]
  show-shource = True

It will change how your reports are formatted,
and will show the exact problem with your code:

.. code::

  » flake8 . --format=wemake --show-source

  ./wemake_python_styleguide/formatter.py

    E231  120:32   missing whitespace after ':'
    def show_source(self, error:Violation) -> str:
                              ^

It helps to visially identify the problems in your code and fix it faster.
We include ``show-shource = True`` into our default configuration.


Showing statistic
-----------------

You can also show the statitics about problems inside your code.

It will group all violations by type and tell how many of them
do you have and where you have them:

.. code::

  » flake8 . --format=wemake --show-source --statistic

  ./wemake_python_styleguide/formatter.py

    E231  136:32   missing whitespace after ':'
    def show_source(self, error:Violation) -> str:
                              ^

  ./wemake_python_styleguide/types.py

    E231  52:47    missing whitespace after ','
    AnyFunctionDefAndLambda = Union[AnyFunctionDef,ast.Lambda]
                                                 ^

  E231: missing whitespace after ':'
    1     ./wemake_python_styleguide/formatter.py
    1     ./wemake_python_styleguide/types.py
  Total: 2


  All errors: 2

We do not include ``show-statistic`` in our default configuration.
It should be only called


.. _formatter:

Formatter API
-------------

That's how all ``flake8`` formatters work:

.. mermaid::
   :caption: ``flake8`` formatting API calls order.

    graph LR
        F1[flake8] --> F2[after_init]
        F2         --> F3[handle]
        F3         --> F4[format]
        F3	       --> F5[show_source]
        F3	       --> F6[show_statistic]

.. autoclass:: WemakeFormatter
   :no-undoc-members:

"""

from collections import defaultdict

from flake8.formatting.base import BaseFormatter
from flake8.statistics import Statistics
from flake8.style_guide import Violation
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer


class WemakeFormatter(BaseFormatter):
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

    # API:

    def after_init(self):
        """Called after the original ``init`` is used to set extra fields."""
        self._lexer = PythonLexer()
        self._formatter = TerminalFormatter()
        self._proccessed_filenames = []

    def handle(self, error: Violation) -> None:  # noqa: Z110
        """Processes each :term:`violation` to print it and all related."""
        if error.filename not in self._proccessed_filenames:
            self._print_header(error.filename)
            self._proccessed_filenames.append(error.filename)

        super().handle(error)

    def format(self, error: Violation) -> str:  # noqa: A003
        """Called to format each individual :term:`violation`."""
        return '{newline}  {code:<5} {row_col:<8} {text}'.format(
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

        code = highlight(
            formated_line,
            self._lexer,
            self._formatter,
        )

        return '  {code}  {pointer}^'.format(
            code=code,
            pointer=' ' * (error.column_number - 1 - adjust),
        )

    def show_statistics(self, statistics: Statistics) -> None:  # noqa: Z210
        """Called when ``--statistic`` option is passed."""
        all_errors = 0
        for error_code in statistics.error_codes():
            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)

            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            all_errors += count
            error_by_file = _count_per_filename(statistics, error_code)

            self._write(
                '{newline}{error_code}: {message}'.format(
                    newline=self.newline,
                    error_code=_bold(error_code),
                    message=statistic.message,
                ),
            )
            for filename in error_by_file:
                self._write(
                    '  {error_count:<5} {filename}'.format(
                        error_count=error_by_file[filename],
                        filename=filename,
                    ),
                )
            self._write(_underline('Total: {0}'.format(count)))

        self._write(self.newline)
        self._write(_underline(_bold('All errors: {0}'.format(all_errors))))

    # Our own methods:

    def _print_header(self, filename: str) -> None:
        self._write(
            '{newline}{filename}'.format(
                filename=_underline(_bold(filename)),
                newline=self.newline,
            ),
        )

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


# Helpers:

def _count_per_filename(statistics: Statistics, error_code: str):
    filenames = defaultdict(int)
    stats_for_error_code = statistics.statistics_for(error_code)

    for stat in stats_for_error_code:
        filenames[stat.filename] += stat.count

    return filenames
