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

You might want to also install optional tools
that pairs nicely with ``wemake-python-styleguide``:

- :ref:`flakeheaven` for easy integration into a **legacy** codebase
- :ref:`nitpick` for sharing and validating
  configuration across multiple projects


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

Check out how we do it in our different templates:

- ``django`` and ``gitlab-ci``: https://github.com/wemake-services/wemake-django-template
- ``python`` package and ``travis``: https://github.com/wemake-services/wemake-python-package

.. rubric:: Further reading

- :ref:`Configuring and ignoring violations <configuration>`
- :ref:`Introducing this linter to a legacy codebase <flakeheaven>`
- :ref:`Sharing configuration across multiple projects <nitpick>`
