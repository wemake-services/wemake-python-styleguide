Violations
----------

Here we have all violation codes listed for this plugin and its dependencies.
Our violation codes are using ``WPS`` letters.
Other codes are coming from other tools.


.. rubric:: Our own codes

============== ======
Type           Codes
-------------- ------
System         :ref:`WPS000 - WPS099 <system>`
Naming         :ref:`WPS100 - WPS199 <naming>`
Complexity     :ref:`WPS200 - WPS299 <complexity>`
Consistency    :ref:`WPS300 - WPS399 <consistency>`
Best practices :ref:`WPS400 - WPS499 <best-practices>`
Refactoring    :ref:`WPS500 - WPS599 <refactoring>`
OOP            :ref:`WPS600 - WPS699 <oop>`
============== ======


.. rubric:: External plugins

All codes are sorted alphabetically and by numerical codes.

=============================  ======
Plugin                         Codes
-----------------------------  ------
flake8-bugbear                 `B001 - B008 <https://github.com/PyCQA/flake8-bugbear#list-of-warnings>`_
flake8-comprehensions          `C400 - C411 <https://github.com/adamchainz/flake8-comprehensions>`_
flake8-commas                  `C812 - C819 <https://pypi.org/project/flake8-commas/>`_
mccabe                         `C901 <http://flake8.pycqa.org/en/latest/user/error-codes.html>`_
flake8-docstrings              `D100 - D417 <https://www.pydocstyle.org/en/latest/error_codes.html>`_
pycodestyle                    `E001 - E902, W001 - W606 <http://pycodestyle.pycqa.org/en/latest/intro.html#error-codes>`_
flake8-eradicate               `E800 <https://github.com/sobolevn/flake8-eradicate>`_
flake8                         `F400 - F901 <http://flake8.pycqa.org/en/latest/user/error-codes.html>`_
flake8-isort                   `I001 - I005 <https://github.com/gforcada/flake8-isort/blob/master/flake8_isort.py>`_
flake8-broken-line             `N400 <https://github.com/sobolevn/flake8-broken-line>`_
pep8-naming                    `N800 - N820 <https://github.com/PyCQA/pep8-naming>`_
flake8-string-format           `P101 - P302 <https://github.com/xZise/flake8-string-format#error-codes>`_
flake8-quotes                  `Q000 <https://github.com/zheller/flake8-quotes>`_
flake8-bandit                  `S100 - S710 <https://github.com/tylerwince/flake8-bandit>`_, see also original ``bandit`` `codes <https://bandit.readthedocs.io/en/latest/plugins/index.html#complete-test-plugin-listing>`_
flake8-debugger                `T100 <https://github.com/JBKahn/flake8-debugger/blob/master/flake8_debugger.py>`_
flake8-rst-docstrings          `RST201 - RST499 <https://github.com/peterjc/flake8-rst-docstrings>`_
darglint                       `DAR001 - DAR501 <https://github.com/terrencepreilly/darglint#error-codes>`_
wemake-python-styleguide       WPS, defined here
=============================  ======

.. toctree::
  :maxdepth: 0
  :caption: Violation types:
  :hidden:

  system.rst
  naming.rst
  complexity.rst
  consistency.rst
  best_practices.rst
  refactoring.rst
  oop.rst
