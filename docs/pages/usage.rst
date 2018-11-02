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

See the ``flake8`` docs for `options <http://flake8.pycqa.org/en/latest/user/configuration.html>`_
and `usage examples <http://flake8.pycqa.org/en/latest/user/invocation.html>`_.

Golden rule is to run your linter on each commit locally and inside the CI.
And to fail the build if there are any style violations.

Ignoring violations
-------------------

We know that people might not agree with 100% of our rules.
But we still want to provide the best experience for all users.

So, you can disable some checks, that you are not ok with.

There are three ways to ignore some specific violations:

1. Inline ignore with ``# noqa:`` comment and comma separated violation codes
2. Command line argument ``--ignore`` with omma separated violation codes
3. Configuration line inside ``setup.cfg`` or ``tox.ini``, `example <https://github.com/wemake-services/wemake-python-styleguide/blob/ab95b7d5b14b3985795aa98a70363466fffa3946/setup.cfg#L22-L32>`_

You can ignore:

1. Whole ``Z`` letter, this will completely turn off all our custom checks
2. Some specific group (naming, complexity, consistency, best practices)
   with ``Z`` and the first number
3. Some specific violation with the full violation code

Read more about `ignoring violations <http://flake8.pycqa.org/en/latest/user/violations.html>`_
in the official docs.

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

Extras
------

There are some tools that are out of scope of this linter,
however they are super cool. And should definitely be used!

Things we highly recommend to improve your code quality:

- `mypy <https://github.com/python/mypy>`_ runs type checks on your python code. Finds tons of issues. Makes your code better, improves you as a programmer. You must use, and tell your friends to use it too
- `layer-linter <https://github.com/seddonym/layer_linter>`_ allows you to define application layers and ensure you do not break that contract. Absolutely must have
- `xenon <https://github.com/rubik/xenon>`_ and `radon <https://github.com/rubik/radon>`_ allow you to automate some code metrics check
- `cohesion <https://github.com/mschwager/cohesion>`_ tool to measure code cohesion, works for most of the times. We recommend to use it as a reporting tool
- `vulture <https://github.com/jendrikseipp/vulture>`_ allows you to find unused code. Has some drawbacks, since there is too many magic in python code. But, it is still very useful tool for the refactoring

Uninstall
---------

We do not recommend to uninstall our linter ;)

But, in case you really have to, we can help you with an advice:

- use ``poetry`` or ``pipenv``,
  this way all our dependencies will also be removed alongside the main tool
- if you still use ``pip``,
  you will have to manually delete all the dependencies
  which can be found in project's `pyproject.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/pyproject.toml>`_
