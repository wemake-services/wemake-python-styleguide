.. _usage:

Usage
=====

Remember that ``wemake-python-styleguide`` is just a ``flake8`` plugin.

Running
-------

To run our linter you will need to run ``flake8`` in any way you like:

.. code:: bash

    flake8 your_module.py
    flake8 your_package

See `the official docs <https://github.com/tholo/pytest-flake8>`_
for options and usage examples.

Golden rule is to run your linter on each commit locally and inside the CI.
And to fail the build if there are any style violations.

Integrations
------------

We leverage all the existing ``flake8`` infrastructure.
There are different integrations for your workflow.

Hooks
~~~~~

- `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ to run style checks alongside with tests (**recommended**)
- `pre-commit <https://pre-commit.com/>`_ to run ``flake8`` before all commits locally

Editors
~~~~~~~

- `vscode plugin <https://code.visualstudio.com/docs/python/linting>`_
- `sublime plugin <https://github.com/SublimeLinter/SublimeLinter-flake8>`_
- `atom plugin <https://atom.io/packages/linter-flake8>`_

Uninstall
---------

We do not recommend to uninstall our linter ;)

But, in case you really have to, we can help you with an advice:

- use ``poetry`` or ``pipenv``,
  this way all our dependencies will also be removed alongside the main tool
- if you still use ``pip``,
  you will have to manually delete all the dependencies
  which can be found in project's `pyproject.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/pyproject.toml>`_
