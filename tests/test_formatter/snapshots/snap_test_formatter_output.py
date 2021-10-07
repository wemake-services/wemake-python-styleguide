# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_formatter[cli_options0-regular] formatter_regular'] = '''
./tests/fixtures/formatter/formatter1.py
  1:1      WPS111 Found too short name: s < 2
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

./tests/fixtures/formatter/formatter2.py
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options1-regular_statistic] formatter_regular_statistic'] = '''
./tests/fixtures/formatter/formatter1.py
  1:1      WPS111 Found too short name: s < 2
  1:7      WPS110 Found wrong variable name: handle
  2:21     WPS432 Found magic number: 200
  2:21     WPS303 Found underscored number: 2_00

./tests/fixtures/formatter/formatter2.py
  1:1      WPS110 Found wrong variable name: data
  1:10     WPS110 Found wrong variable name: param
  2:12     WPS437 Found protected attribute usage: _protected
  2:31     WPS303 Found underscored number: 10_00

WPS110: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
Total: 3

WPS111: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS303: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
Total: 2

WPS432: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS437: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
Total: 1


All errors: 8

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options2-with_source] formatter_with_source'] = '''
./tests/fixtures/formatter/formatter1.py

  1:1      WPS111 Found too short name: s < 2
  def s(handle: int) -> int:
  ^

  1:7      WPS110 Found wrong variable name: handle
  def s(handle: int) -> int:
        ^

  2:21     WPS432 Found magic number: 200
  return handle + 2_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  return handle + 2_00
                  ^

./tests/fixtures/formatter/formatter2.py

  1:1      WPS110 Found wrong variable name: data
  def data(param) -> int:
  ^

  1:10     WPS110 Found wrong variable name: param
  def data(param) -> int:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  return param._protected + 10_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  return param._protected + 10_00
                            ^

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options3-with_source_statistic] formatter_with_source_statistic'] = '''
./tests/fixtures/formatter/formatter1.py

  1:1      WPS111 Found too short name: s < 2
  def s(handle: int) -> int:
  ^

  1:7      WPS110 Found wrong variable name: handle
  def s(handle: int) -> int:
        ^

  2:21     WPS432 Found magic number: 200
  return handle + 2_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  return handle + 2_00
                  ^

./tests/fixtures/formatter/formatter2.py

  1:1      WPS110 Found wrong variable name: data
  def data(param) -> int:
  ^

  1:10     WPS110 Found wrong variable name: param
  def data(param) -> int:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  return param._protected + 10_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  return param._protected + 10_00
                            ^

WPS110: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
Total: 3

WPS111: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS303: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
Total: 2

WPS432: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS437: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
Total: 1


All errors: 8

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter[cli_options4-statistic_with_source] formatter_statistic_with_source'] = '''
./tests/fixtures/formatter/formatter1.py

  1:1      WPS111 Found too short name: s < 2
  def s(handle: int) -> int:
  ^

  1:7      WPS110 Found wrong variable name: handle
  def s(handle: int) -> int:
        ^

  2:21     WPS432 Found magic number: 200
  return handle + 2_00
                  ^

  2:21     WPS303 Found underscored number: 2_00
  return handle + 2_00
                  ^

./tests/fixtures/formatter/formatter2.py

  1:1      WPS110 Found wrong variable name: data
  def data(param) -> int:
  ^

  1:10     WPS110 Found wrong variable name: param
  def data(param) -> int:
           ^

  2:12     WPS437 Found protected attribute usage: _protected
  return param._protected + 10_00
         ^

  2:31     WPS303 Found underscored number: 10_00
  return param._protected + 10_00
                            ^

WPS110: Found wrong variable name: handle
  1     ./tests/fixtures/formatter/formatter1.py
  2     ./tests/fixtures/formatter/formatter2.py
Total: 3

WPS111: Found too short name: s < 2
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS303: Found underscored number: 2_00
  1     ./tests/fixtures/formatter/formatter1.py
  1     ./tests/fixtures/formatter/formatter2.py
Total: 2

WPS432: Found magic number: 200
  1     ./tests/fixtures/formatter/formatter1.py
Total: 1

WPS437: Found protected attribute usage: _protected
  1     ./tests/fixtures/formatter/formatter2.py
Total: 1


All errors: 8

Full list of violations and explanations:
https://wemake-python-stylegui.de/en/xx.xx/pages/usage/violations/
'''

snapshots['test_formatter_correct[cli_options0-regular] formatter_correct_regular'] = ''

snapshots['test_formatter_correct[cli_options1-regular_statistic] formatter_correct_regular_statistic'] = '''

All errors: 0
'''

snapshots['test_formatter_correct[cli_options2-with_source] formatter_correct_with_source'] = ''

snapshots['test_formatter_correct[cli_options3-with_source_statistic] formatter_correct_with_source_statistic'] = '''

All errors: 0
'''

snapshots['test_formatter_correct[cli_options4-statistic_with_source] formatter_correct_statistic_with_source'] = '''

All errors: 0
'''

snapshots['test_ipynb formatter_ipynb'] = '''
tests/fixtures/notebook.ipynb
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
https://wemake-python-stylegui.de/en/0.14.1/pages/usage/violations/
'''
