.. _nitpick:

nitpick
-------

``nitpick`` is a tool to lint
your configuration based on existing super rules.

Read the `official docs <https://github.com/andreoliwa/nitpick>`_.
This tool simplifies the configuration changes across multiple projects.

That's how it works. It is a two steps process.

Styleguide repository
~~~~~~~~~~~~~~~~~~~~~

You create a `set of files <https://github.com/wemake-services/wemake-python-styleguide/tree/master/scripts>`_ where you describe what configuration must be contained for each tool you use. You also create a master `nitpick-style.toml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/nitpick-style.toml>`_ where you list all the styles in a single place

Project repository
~~~~~~~~~~~~~~~~~~

You install ``nitpick`` and specify the path to your
super ``nitpick-style.toml`` file inside your ``pyproject.toml``:

.. code:: toml

  [tool.nitpick]
  style = "https://github.com/wemake-services/wemake-python-styleguide/blob/master/nitpick-style.toml"

Now when you will run ``flake8`` your configuration will be also linted.
And by "linted" we mean that it will check that all required keys
and values are in place in the correct files.

Partial configs
~~~~~~~~~~~~~~~

You can also include only some configs if you don't use some tools for example:

.. code:: toml

  [tool.nitpick]
  style = [
    "https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/flake8.toml",
    "https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/isort.toml"
  ]

This way you can include only some parts of the global preset.

Support
~~~~~~~

``wemake-python-styleguide`` officially supports ``nitpick``
and by this we mean that we have our configuration preset
and also run ``nitpick`` on our own configuration on each build.

We only put the essential configuration in the default preset.
It is limited to the best-practices and configuration correctness.
It is not limited to stylistic choices or complexity settings.
