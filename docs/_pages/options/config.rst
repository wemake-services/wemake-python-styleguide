Config
------

.. automodule:: wemake_python_styleguide.options.config
   :members:

Defaults
~~~~~~~~

.. automodule:: wemake_python_styleguide.options.defaults
   :members:

Third party plugins
~~~~~~~~~~~~~~~~~~~

It is also important to configure different plugins that we ship with
this module.

.. code:: ini

    [flake8]
    max-complexity = 6
    max-line-length = 80

    # Flake plugins:
    inline-quotes = single
    accept-encodings = utf-8

Place this configuration inside ``setup.cfg`` file.
Our repository contains the full working example.

We also use ``flake8-isort`` to style our imports.
You will need to update your configuration with the following lines:

.. code:: ini

      [isort]
      # See https://github.com/timothycrosley/isort#multi-line-output-modes
      multi_line_output = 3
      include_trailing_comma = true
      sections = FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER
      default_section = FIRSTPARTY

Otherwise, your ``isort`` will complain about your imports.
