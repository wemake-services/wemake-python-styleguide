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


Ignoring violations
-------------------

We know that people might not agree with 100% of our rules.
But we still want to provide the best experience for all users.

So, you can disable some checks, that you are not ok with.
**Note**: you might accidentally break the consistency of this project,
when you disable some checks.
`Report <https://github.com/wemake-services/wemake-python-styleguide/issues>`_
these cases.

There are three ways to ignore some specific violations:

1. Inline ignore with ``# noqa:`` comment and comma separated violation codes
2. Command line argument ``--ignore`` with comma separated violation codes
3. Configuration line inside ``setup.cfg`` or ``tox.ini``, `example <https://github.com/wemake-services/wemake-python-styleguide/blob/master/setup.cfg#L23-L36>`_

You can ignore:

1. Whole ``WPS`` letters, this will completely turn off all our custom checks
2. Some specific group (naming, complexity, consistency, best practices, etc)
   with ``WPS`` and the first number of this group
3. Some specific violation with the full violation code

Use `per-file-ignores <https://flake8.pycqa.org/en/latest/user/options.html?highlight=per-file-ignores#cmdoption-flake8-per-file-ignores>`_
option, so it is possible to ignore violations on a per-file bases.
It means, that you can have different set of violations
ignored for different files.

Example:

.. code:: ini

  # contents of setup.cfg

  [flake8]
  per-file-ignores =
    # There are multiple `assert`s in tests, we allow them:
    tests/*.py: S101

Read more about `ignoring violations <http://flake8.pycqa.org/en/latest/user/violations.html>`_
in the official docs.
