# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter[cli_options0-regular] formatter_regular'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m
  1:1      WPS111 Found too short name: s < 2
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options1-regular_statistic] formatter_regular_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m
  1:1      WPS111 Found too short name: s < 2
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options2-with_source] formatter_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s < 2
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                            ^

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options3-with_links] formatter_with_links'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m
  1:1      WPS111 Found too short name: s < 2
           -> https://pyflak.es/WPS111
  1:7      WPS110 Found wrong variable name: handle
           -> https://pyflak.es/WPS110
  2:21     WPS432 Found magic number: 200
           -> https://pyflak.es/WPS432
  2:21     WPS303 Found underscored number: 2_00
           -> https://pyflak.es/WPS303

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m
  1:1      WPS110 Found wrong variable name: data
           -> https://pyflak.es/WPS110
  1:10     WPS110 Found wrong variable name: param
           -> https://pyflak.es/WPS110
  2:12     WPS437 Found protected attribute usage: _protected
           -> https://pyflak.es/WPS437
  2:31     WPS303 Found underscored number: 10_00
           -> https://pyflak.es/WPS303

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options4-with_source_statistic] formatter_with_source_statistic'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s < 2
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                            ^

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options5-with_source_links] formatter_with_source_links'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s < 2
           -> https://pyflak.es/WPS111
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:7      WPS110 Found wrong variable name: handle
           -> https://pyflak.es/WPS110
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
        ^

  2:21     WPS432 Found magic number: 200
           -> https://pyflak.es/WPS432
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

  2:21     WPS303 Found underscored number: 2_00
           -> https://pyflak.es/WPS303
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
           -> https://pyflak.es/WPS110
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:10     WPS110 Found wrong variable name: param
           -> https://pyflak.es/WPS110
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
           ^

  2:12     WPS437 Found protected attribute usage: _protected
           -> https://pyflak.es/WPS437
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
         ^

  2:31     WPS303 Found underscored number: 10_00
           -> https://pyflak.es/WPS303
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                            ^

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options6-statistic_with_source] formatter_statistic_with_source'] = '''
\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter1.py\x1b[0m\x1b[0m

  1:1      WPS111 Found too short name: s < 2
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:7      WPS110 Found wrong variable name: handle
  \x1b[34mdef\x1b[39;49;00m \x1b[32ms\x1b[39;49;00m(handle: \x1b[36mint\x1b[39;49;00m) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
        ^

  2:21     WPS432 Found magic number: 200
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

  2:21     WPS303 Found underscored number: 2_00
  \x1b[34mreturn\x1b[39;49;00m handle + \x1b[34m2_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                  ^

\x1b[4m\x1b[1m./tests/fixtures/formatter/formatter2.py\x1b[0m\x1b[0m

  1:1      WPS110 Found wrong variable name: data
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
  ^

  1:10     WPS110 Found wrong variable name: param
  \x1b[34mdef\x1b[39;49;00m \x1b[32mdata\x1b[39;49;00m(param) -> \x1b[36mint\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
         ^

  2:31     WPS303 Found underscored number: 10_00
  \x1b[34mreturn\x1b[39;49;00m param._protected + \x1b[34m10_00\x1b[39;49;00m\x1b[37m\x1b[39;49;00m
                            ^

\x1b[1mWPS110\x1b[0m: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 3\x1b[0m

\x1b[1mWPS111\x1b[0m: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS303\x1b[0m: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 2\x1b[0m

\x1b[1mWPS432\x1b[0m: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
\x1b[4mTotal: 1\x1b[0m

\x1b[1mWPS437\x1b[0m: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
\x1b[4mTotal: 1\x1b[0m


\x1b[4m\x1b[1mAll errors: 8\x1b[0m\x1b[0m

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter_correct[cli_options0-regular] formatter_correct_regular'] = ''

snapshots['test_formatter_correct[cli_options1-regular_statistic] formatter_correct_regular_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options2-with_source] formatter_correct_with_source'] = ''

snapshots['test_formatter_correct[cli_options3-with_links] formatter_correct_with_links'] = ''

snapshots['test_formatter_correct[cli_options4-with_source_statistic] formatter_correct_with_source_statistic'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_formatter_correct[cli_options5-with_source_links] formatter_correct_with_source_links'] = ''

snapshots['test_formatter_correct[cli_options6-statistic_with_source] formatter_correct_statistic_with_source'] = '''

\x1b[4m\x1b[1mAll errors: 0\x1b[0m\x1b[0m
'''

snapshots['test_ipynb formatter_ipynb'] = '''
\x1b[4m\x1b[1mtests/fixtures/notebook.ipynb\x1b[0m\x1b[0m
  3:1      DAR101 Missing parameter(s) in Docstring: - good_name
  3:1      DAR201 Missing "Returns" in Docstring: - return
  8:1      D103  Missing docstring in public function
  8:1      WPS111 Found too short name: s < 2
  8:7      WPS110 Found wrong variable name: handle
  9:21     WPS432 Found magic number: 200
  9:21     WPS303 Found underscored number: 2_00
  13:1     D103  Missing docstring in public function
  13:1     WPS110 Found wrong variable name: data
  13:10    WPS110 Found wrong variable name: param
  14:12    WPS437 Found protected attribute usage: _protected
  14:31    WPS303 Found underscored number: 10_00

Full list of violations and explanations:
https://wemake-python-styleguide.rtfd.io/en/xx.xx/pages/usage/violations/
'''
