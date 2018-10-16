Config
======

.. automodule:: wemake_python_styleguide.options.config
   :members:

Defaults
--------

.. automodule:: wemake_python_styleguide.options.defaults
   :members:

Plugins
-------

It is also important to configure different plugins that we ship with
this module.

.. code:: ini

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

      [isort]
      multi_line_output = 3
      include_trailing_comma = true
      default_section = FIRSTPARTY
      line_length = 80

Otherwise, your ``isort`` will complain about your imports.

We are working hard to remove any kind of configuration from this tool.
Please, be calm!
