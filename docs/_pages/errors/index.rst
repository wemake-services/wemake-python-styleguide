Errors
======

Here we have all error codes listed for this plugin and all its dependencies.
Our error codes are using ``Z`` letter.
Other codes are coming from other tools.

All codes are sorted alphabetically and by numerical codes.

========================  ======
Plugin                    Codes
------------------------  ------
flake8-builtins           `A001 - A002 <https://github.com/gforcada/flake8-builtins/blob/master/flake8_builtins.py>`_
flake8-bugbear            `B001 - B008 <https://github.com/PyCQA/flake8-bugbear#list-of-warnings>`_
flake8-coding             `C101 - C103 <https://github.com/tk0miya/flake8-coding#rules>`_
flake8-comprehensions     `C400 - C411 <https://github.com/adamchainz/flake8-comprehensions>`_
flake8-commas             `C812 - C819 <https://pypi.org/project/flake8-commas/>`_
mccabe                    `C901 <http://flake8.pycqa.org/en/latest/user/error-codes.html>`_
flake8-docstrings         `D100 - D414 <http://www.pydocstyle.org/en/2.1.1/error_codes.html>`_
pycodestyle               `E001 - E902, W001 - W606 <http://pycodestyle.pycqa.org/en/latest/intro.html#error-codes>`_
flake8-eradicate          `E800 <https://github.com/sobolevn/flake8-eradicate>`_
flake8                    `F400 - F901 <http://flake8.pycqa.org/en/latest/user/error-codes.html>`_
flake8-logging-format     `G001 - G202 <https://github.com/globality-corp/flake8-logging-format>`_
flake8-isort              `I001 - I005 <https://github.com/gforcada/flake8-isort/blob/master/flake8_isort.py>`_
pep8-naming               `N800 - N820 <https://github.com/PyCQA/pep8-naming>`_
flake8-string-format      `P101 - P302 <https://github.com/xZise/flake8-string-format#error-codes>`_
flake8-quotes             `Q000 <https://github.com/zheller/flake8-quotes>`_
flake8-pep3101            `S001 <https://github.com/gforcada/flake8-pep3101/blob/master/flake8_pep3101.py>`_
flake8-bandit             `S100 - S710 <https://github.com/tylerwince/flake8-bandit>`_, see also original ``bandit`` `codes <https://bandit.readthedocs.io/en/latest/plugins/index.html#complete-test-plugin-listing>`_
flake8-debugger           `T100 <https://github.com/JBKahn/flake8-debugger/blob/master/flake8_debugger.py>`_
flake8-type-annotations   `T800 - T801 <https://github.com/sobolevn/flake8-type-annotations#error-codes>`_
wemake-python-styleguide  Z, defined here
========================  ======

Our own codes are the following ones:

=========== ======
Plugin      Codes
----------- ------
Tokens      :ref:`Z001 - Z099 <tokens>`
Imports     :ref:`Z100 - Z109 <imports>`
General     :ref:`Z110 - Z199 <general>`
Complexity  :ref:`Z200 - Z299 <complexity>`
Classes     :ref:`Z300 - Z399 <classes>`
Modules     :ref:`Z400 - Z499 <modules>`
=========== ======

.. toctree::
  :maxdepth: 1
  :caption: Error types:
  :hidden:

  tokens.rst
  imports.rst
  general.rst
  classes.rst
  complexity.rst
  modules.rst
