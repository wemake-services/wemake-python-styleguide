Setup
=====

Remember that ``wemake-python-styleguide`` is just a ``flake8`` plugin.

.. _usage:

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
**Note**: you might accidentally break the consistency of this project,
when you disable some checks. We **do not** officially recommend to do it.

There are three ways to ignore some specific violations:

1. Inline ignore with ``# noqa:`` comment and comma separated violation codes
2. Command line argument ``--ignore`` with comma separated violation codes
3. Configuration line inside ``setup.cfg`` or ``tox.ini``, `example <https://github.com/wemake-services/wemake-python-styleguide/blob/master/setup.cfg#L23-L36>`_

You can ignore:

1. Whole ``WPS`` letters, this will completely turn off all our custom checks
2. Some specific group (naming, complexity, consistency, best practices)
   with ``WPS`` and the first number of this group
3. Some specific violation with the full violation code

Use `per-file-ignores <https://flake8.pycqa.org/en/latest/user/options.html?highlight=per-file-ignores#cmdoption-flake8-per-file-ignores>`_
option, so it is possible to ignore violations on a per-file bases.
It means, that you can have different set of violations
ignored for different files.

Read more about `ignoring violations <http://flake8.pycqa.org/en/latest/user/violations.html>`_
in the official docs.

Legacy projects
---------------

Introducing this package to a legacy project is almost impossible.
Due to strict quality, consistency, and complexity rules.

But, you still can do several things to integrate this linter step by step:

1. Fix consistency, naming and best-practices violations,
   they are the easiest to clean up.
2. Per-file ignore complexity checks that are failing for your project.
   Sometimes it is possible to rewrite several parts of your code,
   but generally complexity rules are the hardest to fix.
3. Use `boyscout rule <https://deviq.com/boy-scout-rule/>`_: always leave
   your code better than you found it.

You can also only lint `recently changed files <https://github.com/getsentry/raven-python/blob/master/hooks/pre-commit.flake8>`_.

You can also use `--diff option <http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-diff>`_
of ``flake8`` to lint the latest changes only.
This might have different errors,
and this mode is not officially supported for now.
