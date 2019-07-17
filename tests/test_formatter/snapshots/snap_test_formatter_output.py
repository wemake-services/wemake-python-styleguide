# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter[cli_options0-regular] formatter_regular'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  Z111  1:1      Found too short name: s
  Z110  1:7      Found wrong variable name: handle
  Z432  2:21     Found magic number: 200
  Z303  2:21     Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  Z110  1:1      Found wrong variable name: data
  Z110  1:10     Found wrong variable name: param
  Z441  2:12     Found protected attribute usage: _protected
  Z303  2:31     Found underscored number: 10_00

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/0.10.0/pages/violations/
'''

snapshots['test_formatter[cli_options4-statistic_with_source] formatter_statistic_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  Z111  1:1      Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:7      Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  Z432  2:21     Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  Z303  2:21     Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  Z110  1:1      Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:10     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  Z441  2:12     Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  Z303  2:31     Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mZ111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mZ432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ441\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/0.10.0/pages/violations/
'''

snapshots['test_formatter[cli_options3-with_source_statistic] formatter_with_source_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  Z111  1:1      Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:7      Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  Z432  2:21     Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  Z303  2:21     Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  Z110  1:1      Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:10     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  Z441  2:12     Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  Z303  2:31     Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mZ111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mZ432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ441\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/0.10.0/pages/violations/
'''

snapshots['test_formatter[cli_options2-with_source] formatter_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  Z111  1:1      Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:7      Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  Z432  2:21     Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  Z303  2:21     Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  Z110  1:1      Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  Z110  1:10     Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  Z441  2:12     Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  Z303  2:31     Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/0.10.0/pages/violations/
'''

snapshots['test_formatter[cli_options1-regular_statistic] formatter_regular_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  Z111  1:1      Found too short name: s
  Z110  1:7      Found wrong variable name: handle
  Z432  2:21     Found magic number: 200
  Z303  2:21     Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  Z110  1:1      Found wrong variable name: data
  Z110  1:10     Found wrong variable name: param
  Z441  2:12     Found protected attribute usage: _protected
  Z303  2:31     Found underscored number: 10_00

\x1b[1mZ110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mZ111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mZ432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mZ441\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/0.10.0/pages/violations/
'''

snapshots['test_formatter_correct[cli_options1-regular_statistic] formatter_correct_regular_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options0-regular] formatter_correct_regular'] = ''

snapshots['test_formatter_correct[cli_options2-with_source] formatter_correct_with_source'] = ''

snapshots['test_formatter_correct[cli_options3-with_source_statistic] formatter_correct_with_source_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options4-statistic_with_source] formatter_correct_statistic_with_source'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''
