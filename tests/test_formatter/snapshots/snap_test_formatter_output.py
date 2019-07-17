# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter[cli_options0-regular] formatter_regular'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  C101  1:1      Coding magic comment not found
  D100  1:1      Missing docstring in public module
  Z110  1:25     Found wrong variable name: handle
  E225  1:37     missing whitespace around operator
  D401  2:1      First line should be in imperative mood; try rephrasing
  E225  3:20     missing whitespace around operator

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  C101  1:1      Coding magic comment not found
  D100  1:1      Missing docstring in public module
  D103  1:1      Missing docstring in public function
  Z110  1:19     Found wrong variable name: param
  E231  1:24     missing whitespace after ':'
  E225  1:32     missing whitespace around operator
'''

snapshots['test_formatter[cli_options4-statistic_with_source] formatter_statistic_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:25     Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                          ^

  E225  1:37     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                                      ^

  D401  2:1      First line should be in imperative mood; try rephrasing
  \x1b[33m"""This one has a docstring."""\x1b[39;49;00m
  ^

  E225  3:20     missing whitespace around operator
  \x1b[34mreturn\x1b[39;49;00m handle +\x1b[34m2\x1b[39;49;00m
                 ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D103  1:1      Missing docstring in public function
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:19     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                    ^

  E231  1:24     missing whitespace after ':'
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                         ^

  E225  1:32     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                                 ^

\x1b[1mC101\x1b[0m: Coding magic comment not found
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD100\x1b[0m: Missing docstring in public module
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD103\x1b[0m: Missing docstring in public function
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mD401\x1b[0m: First line should be in imperative mood; try rephrasing
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mE225\x1b[0m: missing whitespace around operator
  2     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mE231\x1b[0m: missing whitespace after ':'
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m


\x1b[4m\x1b[1mAll errors: 12\x1b[0m\x1b[0m
'''

snapshots['test_formatter[cli_options3-with_source_statistic] formatter_with_source_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:25     Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                          ^

  E225  1:37     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                                      ^

  D401  2:1      First line should be in imperative mood; try rephrasing
  \x1b[33m"""This one has a docstring."""\x1b[39;49;00m
  ^

  E225  3:20     missing whitespace around operator
  \x1b[34mreturn\x1b[39;49;00m handle +\x1b[34m2\x1b[39;49;00m
                 ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D103  1:1      Missing docstring in public function
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:19     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                    ^

  E231  1:24     missing whitespace after ':'
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                         ^

  E225  1:32     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                                 ^

\x1b[1mC101\x1b[0m: Coding magic comment not found
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD100\x1b[0m: Missing docstring in public module
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD103\x1b[0m: Missing docstring in public function
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mD401\x1b[0m: First line should be in imperative mood; try rephrasing
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mE225\x1b[0m: missing whitespace around operator
  2     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mE231\x1b[0m: missing whitespace after ':'
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m


\x1b[4m\x1b[1mAll errors: 12\x1b[0m\x1b[0m
'''

snapshots['test_formatter[cli_options2-with_source] formatter_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:25     Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                          ^

  E225  1:37     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_other_function\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m)->\x1b[36mint\x1b[39;49;00m:
                                      ^

  D401  2:1      First line should be in imperative mood; try rephrasing
  \x1b[33m"""This one has a docstring."""\x1b[39;49;00m
  ^

  E225  3:20     missing whitespace around operator
  \x1b[34mreturn\x1b[39;49;00m handle +\x1b[34m2\x1b[39;49;00m
                 ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  C101  1:1      Coding magic comment not found
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D100  1:1      Missing docstring in public module
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  D103  1:1      Missing docstring in public function
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:19     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                    ^

  E231  1:24     missing whitespace after ':'
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                         ^

  E225  1:32     missing whitespace around operator
  \x1b[34mdef\x1b[39;49;00m \x1b[32msome_function\x1b[39;49;00m(param:\x1b[36mint\x1b[39;49;00m) ->\x1b[36mint\x1b[39;49;00m:
                                 ^
'''

snapshots['test_formatter[cli_options1-regular_statistic] formatter_regular_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  C101  1:1      Coding magic comment not found
  D100  1:1      Missing docstring in public module
  Z110  1:25     Found wrong variable name: handle
  E225  1:37     missing whitespace around operator
  D401  2:1      First line should be in imperative mood; try rephrasing
  E225  3:20     missing whitespace around operator

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  C101  1:1      Coding magic comment not found
  D100  1:1      Missing docstring in public module
  D103  1:1      Missing docstring in public function
  Z110  1:19     Found wrong variable name: param
  E231  1:24     missing whitespace after ':'
  E225  1:32     missing whitespace around operator

\x1b[1mC101\x1b[0m: Coding magic comment not found
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD100\x1b[0m: Missing docstring in public module
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mD103\x1b[0m: Missing docstring in public function
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mD401\x1b[0m: First line should be in imperative mood; try rephrasing
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mE225\x1b[0m: missing whitespace around operator
  2     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mE231\x1b[0m: missing whitespace after ':'
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m


\x1b[4m\x1b[1mAll errors: 12\x1b[0m\x1b[0m
'''
