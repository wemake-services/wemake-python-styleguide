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
