flakehell
---------

.. image:: https://raw.githubusercontent.com/life4/flakehell/master/assets/logo.png

`flakehell <https://github.com/life4/flakehell>`_ is a legacy-first
wrapper around ``flake8`` linter to make it awesome.

What does it mean? It means, that it adds some useful
features to the core ``flake8`` with the new command line utility:

.. code:: bash

  pip install flakehell  # however we recommend to use `poetry`
  flakehell lint  # accepts the same arguments, does the same as `flake8`

The most exiting feature for us is ``baseline`` generation.

.. _flakehell-legacy:

Legacy first
~~~~~~~~~~~~

When you project is old you cannot just install and use a new linter.
Since your codebase will contain hundreds or even thousands of violations.

Some of them can be auto-formatted, some of them can be silenced.
But, what if there are still too many of them to fix right here and right now?

Let me introduce the ``baseline`` concept:

1. The first step is to create a ``baseline`` via:

   .. code:: bash

     flakehell baseline > .flakehell_baseline

   It will contain all your current violations list
   with exact locations and quantity.
2. Then specify the ``baseline`` in the configuration:

   .. code:: ini

     # Inside your pyproject.toml
     [tool.flakehell]
     baseline = ".flakehell_baseline"

3. Run your linter again with ``flakehell lint``. You will see no violations!
4. Try to add a new one into your source code.
   And run your linter again. It will be reported!

The ``baseline`` method allows you to report any new violations
and fix the old ones little by little.
So, the integration is almost painless.

That's why we call it "legacy-first".
Enjoy your new linter in your old project!

Support
~~~~~~~

``flakehell`` is officially supported by ``wemake-python-styleguide``
and developed by the same people.

Further reading
~~~~~~~~~~~~~~~

- Official docs: `flakehell.readthedocs.io <https://flakehell.readthedocs.io>`_
