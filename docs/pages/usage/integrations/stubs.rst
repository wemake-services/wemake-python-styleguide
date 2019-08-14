Stubs
-----

If you are using stub ``.pyi`` files
and `flake8-pyi <https://github.com/ambv/flake8-pyi>`_ extension
you might need to ignore several violations that are bundled with this linter.

You can still do it on per-file bases as usual.
Use ``*.pyi`` glob to list ignored violations:

.. code:: ini

  # Inside `setup.cfg`:
  [flake8]
  per-file-ignores =
    *.pyi: WPS428, WPS604

You can look at the `returns <https://github.com/dry-python/returns>`_
project as an example.
