Setup
=====

Remember that ``wemake-python-styleguide`` is just a ``flake8`` plugin.


.. _installation:

Installation
------------

.. code:: bash

  pip install wemake-python-styleguide

We also recommend to use `poetry <https://github.com/sdispater/poetry>`_
instead of a default ``pip``.

You might want to also intsall optional tools
that pairs nicely with ``wemake-python-styleguide``:

- :ref:`flakehell` for easy integration into a **legacy** codebase
- :ref:`nitpick` for sharing configuration across multiple projects


.. _usage:

Running
-------

To run our linter you will need to run ``flake8`` in any way you like:

.. code:: bash

  flake8 .  # runs on all python files in the current directory (recommended)
  flake8 your_module.py  # runs on a single file
  flake8 your_package  # runs on a single your_package

See the ``flake8`` docs for `options <http://flake8.pycqa.org/en/latest/user/configuration.html>`_
and `usage examples <http://flake8.pycqa.org/en/latest/user/invocation.html>`_.

Golden rule is to run your linter on each commit locally and inside the CI.
And to fail the build if there are any style violations.

Check out how we do it in our ``django`` and ``gitlab-ci`` template:
https://github.com/wemake-services/wemake-django-template

.. rubric:: Further reading

- :ref:`Configuring and ignoring violations <configuration>`
- :ref:`Intoducing this linter to a legacy codebase <flakehell>`
- :ref:`Sharing configuration across multiple projects <nitpick>`
