.. _flakeheaven:

flakeheaven
-----------

``flakeheaven`` is a `legacy-first <https://github.com/flakeheaven/flakeheaven>`_
wrapper around ``flake8`` linter to make it awesome.

What does it mean? It means, that it adds some useful
features to the core ``flake8`` with the new command line utility:

.. code:: bash

  pip install flakeheaven  # however we recommend to use `poetry`

Then you will have to configure ``flakeheaven`` inside your ``pyproject.toml``:

- You can run ``flakeheaven plugins`` to see what plugins are you missing
  and configure it properly
- Or you can use our `preset <https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/flakeheaven.toml>`_
  as ``base`` configuration like so:

  .. code:: toml

    [tool.flakeheaven]
    # optionally inherit from remote config (or local if you want)
    base = "https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/styles/flakeheaven.toml"

And then:

.. code:: bash

  flakeheaven lint  # accepts the same arguments, does the same as `flake8`

The most exciting feature for us is ``baseline`` generation.

.. _flakeheaven-legacy:

Legacy first
~~~~~~~~~~~~

When you project is old you cannot just install and use a new linter.
Since your codebase will contain hundreds or even thousands of violations.

Some of them can be auto-formatted, some of them can be silenced.
But, what if there are still too many of them to fix right here and right now?

Let me introduce the ``baseline`` concept:

1. The first step is to create a ``baseline`` via:

   .. code:: bash

     flakeheaven baseline > .flakeheaven_baseline

   It will contain all your current violations list
   with exact locations and quantity.
2. Then specify the ``baseline`` in the configuration:

   .. code:: ini

     # Inside your pyproject.toml
     [tool.flakeheaven]
     baseline = ".flakeheaven_baseline"

3. Run your linter again with ``flakeheaven lint``. You will see no violations!
4. Try to add a new one into your source code.
   And run your linter again. It will be reported!

The ``baseline`` method allows you to report any new violations
and fix the old ones little by little.
So, the integration is almost painless.

That's why we call it "legacy-first".
Enjoy your new linter in your old project!

Support
~~~~~~~

``flakeheaven`` is officially supported by ``wemake-python-styleguide``
and developed by the same people.

Further reading
~~~~~~~~~~~~~~~

- Our :ref:`legacy` guide
- Official docs: `flakeheaven.readthedocs.io <https://flakeheaven.readthedocs.io>`_
