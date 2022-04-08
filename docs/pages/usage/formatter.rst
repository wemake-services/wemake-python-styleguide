Formatter
=========

Custom formatter for ``flake8`` :term:`violations <violation>`.

Tries to be beautiful, compact, and informative.
Improves the default formatter used by ``flake8``.


.. rubric:: Usage

To activate this formatter one will need to run:

.. code:: bash

  flake8 --format=wemake your_module.py

Or set the configuration option inside ``setup.cfg`` file:

.. code:: ini

  [flake8]
  format = wemake

Option ``format = wemake`` is included into our default configuration.

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/running.png

To switch back to the default ``flake8`` formatter,
you can use ``format = default`` option.

There are other formatters out there as well.
They can be installed as plugins.


.. rubric:: Showing source code

You can also (and we recommend to) enable ``--show-source`` option.
It can be passed as a command line argument or set in ``setup.cfg``:

.. code:: ini

  [flake8]
  show-source = True

It will change how your reports are formatted,
and will show the exact problem with your code:

.. code::

  » flake8 . --format=wemake --show-source

  ./wemake_python_styleguide/formatter.py

    107:32   E231  missing whitespace after ':'
    def show_source(self, error:Violation) -> str:
                               ^

It helps to visually identify the problems in your code and fix it faster.
We include ``show-source = True`` into our default configuration.


.. rubric:: Showing statistic

You can also show the statistics about problems inside your code.

It will group all violations by type and tell how many of them
do you have and where you have them:

.. code::

  » flake8 . --format=wemake --show-source --statistic

  ./wemake_python_styleguide/formatter.py

    107:32   E231  missing whitespace after ':'
    def show_source(self, error:Violation) -> str:
                               ^

  ./wemake_python_styleguide/types.py

    53:47    E231  missing whitespace after ','
    AnyFunctionDefAndLambda = Union[AnyFunctionDef,ast.Lambda]
                                                  ^

  E231: missing whitespace after ':'
    1     ./wemake_python_styleguide/formatter.py
    1     ./wemake_python_styleguide/types.py
  Total: 2


  All errors: 2

We do not include ``show-statistic`` in our default configuration.
It should be only called when user needs to find how many violations
there are and what files do contain them.


.. rubric:: Showing links to documentation

You can also show links to the documentation pages of violations:

.. code::

  » flake8 . --format=wemake --show-source --show-violation-links

  ./wemake_python_styleguide/formatter.py

    107:32   E231  missing whitespace after ':'
             -> https://pyflak.es/E231
    def show_source(self, error:Violation) -> str:
                               ^

In modern terminals, you can click them to open the respective docs page.

We do not include ``show-violation-links`` in our default configuration.
