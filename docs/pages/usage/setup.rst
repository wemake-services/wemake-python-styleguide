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
that pair nicely with ``wemake-python-styleguide``:

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
And to fail the build if there are any violations.

Check out how we do it in our different templates:

- ``django`` and ``gitlab-ci``: https://github.com/wemake-services/wemake-django-template
- ``python`` package and ``travis``: https://github.com/wemake-services/wemake-python-package


Incremental adoption
--------------------

A very popular use-case is when you already
have a relatively large codebase and want to addopt a new linter.

Usually, it is a big pain: you have to spend a lot of time
silencing tens or hundreds of violations.
And you will end up with lots
of silencing individual violations and refactoring.

It is doable, but takes a lot of time.
And makes the adoption of this linter pretty complicated.

Let me introduce you ``--baseline`` option:

.. code:: bash

  flake8 --baseline your_project

Here's what it does:

1. When you run ``--baseline`` mode for the first time
   it will report and record all the violations you have at the moment
   into a new file called ``.flake8-baseline.json``

2. If you try to run the same command once again, it will report no violations.
   Why? Because all of them was saved as existing ones.
   Now linter will report only new violations
   that are not saved into the baseline.

Done! Now you can integrate this linter
into any codebase with just a single command!


.. rubric:: Further reading

- :ref:`Configuring and ignoring violations <configuration>`
- :ref:`Baseline usage <baseline>`
- :ref:`Sharing configuration across multiple projects <nitpick>`
