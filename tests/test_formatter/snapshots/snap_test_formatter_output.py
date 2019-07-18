# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter_correct[cli_options0-regular] formatter_correct_regular'] = ''

snapshots['test_formatter[cli_options2-with_source] formatter_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/violations/
'''

snapshots['test_formatter_correct[cli_options4-statistic_with_source] formatter_correct_statistic_with_source'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options3-with_source_statistic] formatter_correct_with_source_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options1-regular_statistic] formatter_correct_regular_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter[cli_options3-with_source_statistic] formatter_with_source_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/violations/
'''

snapshots['test_formatter[cli_options4-statistic_with_source] formatter_statistic_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2\x1b[39;49;00m_00
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10\x1b[39;49;00m_00
                            ^

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/violations/
'''

snapshots['test_formatter[cli_options0-regular] formatter_regular'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  1:1      WPS111 Found too short name: s
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/violations/
'''

snapshots['test_formatter[cli_options1-regular_statistic] formatter_regular_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter1.py\x1b[0m\x1b[0m
  1:1      WPS111 Found too short name: s
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter2.py\x1b[0m\x1b[0m
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter1.py
  2     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter1.py
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/violations/
'''

snapshots['test_formatter_correct[cli_options2-with_source] formatter_correct_with_source'] = ''
