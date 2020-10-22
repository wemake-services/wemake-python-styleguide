.. _configuration:

Configuration
=============

Before going any further, make sure
that you are familiar with ``flake8``
`configuration process <https://flake8.pycqa.org/en/latest/user/configuration.html>`_.

By default we encourage everyone to use ``setup.cfg`` to store all
the configuration to all ``python`` projects.

.. rubric:: Shareable configurations

If you need to make sure that all projects share the same configuration
you might be interested in :ref:`nitpick` tool to lint your config.
We highly recommend to use ``nitpick`` together
with ``wemake-python-styleguide``.

.. rubric:: Configuring

.. automodule:: wemake_python_styleguide.options.config
   :no-members:

.. rubric:: Plugins

.. note::

  Remember to check the configuration with :ref:`nitpick`.

It is also important to configure different plugins that we ship with
this module.

You can basically configure them as you wish,
including stylistic (like ``--quotes`` from ``flake8-quotes``)
and important things (like ``--max-complexity`` from ``mccabe``).
Our `flake8.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/flake8.toml>`_
file is available with the core settings for ``flake8``.

We also use ``flake8-isort`` to style our imports.
You will need to update your configuration with the following lines:
Otherwise, your ``isort`` will complain about your imports.
Our `isort.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/isort.toml>`_
file is available with the core settings for ``isort``.

All recommended settings can be found in our `styleguide.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/styleguide.toml>`_.

.. rubric:: Ignoring violations

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
3. Configuration line inside ``setup.cfg``, `example <https://github.com/wemake-services/wemake-python-styleguide/blob/master/setup.cfg#L23-L36>`_

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

  # Inside `setup.cfg`:
  [flake8]
  per-file-ignores =
    # There are multiple `assert`s in tests, we allow them:
    tests/*.py: S101

.. rubric:: Further reading

Read more about `ignoring violations <http://flake8.pycqa.org/en/latest/user/violations.html>`_
in the official ``flake8`` docs.
