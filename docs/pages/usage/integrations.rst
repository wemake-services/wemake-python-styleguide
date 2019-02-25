Integrations
============

We leverage all the existing ``flake8`` infrastructure.
There are different integrations for your workflow.

Hooks
-----

- `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ to run style checks alongside with tests
- `pre-commit <https://pre-commit.com/>`_ to run ``flake8`` before all commits locally

Editors
-------

- `vscode plugin <https://code.visualstudio.com/docs/python/linting>`_
- `sublime plugin <https://github.com/SublimeLinter/SublimeLinter-flake8>`_
- `atom plugin <https://atom.io/packages/linter-flake8>`_

Extras
------

There are some tools that are out of scope of this linter,
however they are super cool. And should definitely be used!

Things we highly recommend to improve your code quality:

- `mypy <https://github.com/python/mypy>`_ runs type checks on your python code. Finds tons of issues. Makes your code better, improves you as a programmer. You must use, and tell your friends to use it too
- `layer-linter <https://github.com/seddonym/layer_linter>`_ allows you to define application layers and ensure you do not break that contract. Absolutely must have
- `xenon <https://github.com/rubik/xenon>`_ and `radon <https://github.com/rubik/radon>`_ allow you to automate some code metrics check
- `cohesion <https://github.com/mschwager/cohesion>`_ tool to measure code cohesion, works for most of the times. We recommend to use it as a reporting tool
- `vulture <https://github.com/jendrikseipp/vulture>`_ allows you to find unused code. Has some drawbacks, since there is too many magic in python code. But, it is still very useful tool for the refactoring

Stubs
-----

If you are using stub ``.pyi`` files
and `flake8-pyi <https://github.com/ambv/flake8-pyi>`_ extensions
you might need to ignore several violations that are bundled with this linter.

You can still do it on per-file bases as usual.
Use ``*.pyi`` glob to list ignored violations:

.. code:: cfg

  per-file-ignores =
    *.pyi Z444, Z452

You can look at the `returns <https://github.com/dry-python/returns>`_
project as an example.
