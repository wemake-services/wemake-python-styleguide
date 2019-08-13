Configuration
=============

Before going any further, make sure
that you are familiar with ``flake8``
`configuration process <https://flake8.pycqa.org/en/latest/user/configuration.html>`_.

By default we encourage everyone to use ``setup.cfg`` to store all
the configuration to all ``python`` projects.

.. autoclass:: wemake_python_styleguide.options.config.Configuration
   :no-members:

.. rubric:: Defaults

.. automodule:: wemake_python_styleguide.options.defaults
   :members:

.. rubric:: Plugins

It is also important to configure different plugins that we ship with
this module.

.. code:: ini

  # Inside `setup.cfg`:
  [flake8]
  max-complexity = 6
  max-line-length = 80
  enable-extensions = G

Place this configuration inside ``setup.cfg`` file.
Our repository `contains <https://github.com/wemake-services/wemake-python-styleguide/blob/master/setup.cfg>`_
the fully working example.

We also use ``flake8-isort`` to style our imports.
You will need to update your configuration with the following lines:

.. code:: ini

  # Inside `setup.cfg`:
  [isort]
  multi_line_output = 3
  include_trailing_comma = true
  default_section = FIRSTPARTY
  # Is the same as 80 in flake8:
  line_length = 79

Otherwise, your ``isort`` will complain about your imports.

We are working hard to remove any kind of configuration from this tool.
Please, be calm!

.. rubric:: Sharing the same configuration accross multiple projects

If you need to make sure that all projects share the same configuration
you might be interested in :ref:`nitpick` tool to lint your config.
We highly recommend to use ``nitpick`` together
with ``wemake-python-styleguide``.
