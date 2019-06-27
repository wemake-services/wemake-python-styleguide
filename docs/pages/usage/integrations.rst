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
    *.pyi: Z444, Z452

You can look at the `returns <https://github.com/dry-python/returns>`_
project as an example.

pylint
------

We are not related to the ``pylint`` project.
Yes, we know that it is awesome. But, it has some drawbacks:

1. It makes a lot of type assertions. And does it incorrectly.
   Since we use ``mypy`` there is no sense in this feature.
   Without this feature a lot
   of other ``pylint`` features looses its point as well
2. There are less exisitng plugins for ``pylint`` than for ``flake8``
3. It uses custom ``ast`` parser and library, which can be problematic
4. It is not strict enough for us.
   So, we will have to write our own plugin no matter what platform we use

However, it is important to mention
that ``pylint`` is less radical and more classic in its rules.


black
-----

Is not compatible to ``black``. Let's go deeper and see why.

``black`` is a very simple tool to do just a one thing:
reformat some basic stuff in your code like quotes, commas, and line length.

It is not a linter, but an auto-formatter. And quite an opinionated one!
It is actually not compatible with ``PEP8`` and ``flake8``
(`docs <https://black.readthedocs.io/en/stable/the_black_code_style.html?highlight=flake8>`_),
that's why it is not compatible with ``wemake-python-styleguide`` either.
The difference between a linter and auto-formatter is huge:

- auto-formatters pretties your code a little bit
- linters force you to write beautiful and correct code

For example, auto-formatters won't tell you that your code is too complex.
When your linter will (in case it is a good linter).

We in ``wemake.services`` believe that these kind of tools are not required,
because a good linter will just not let your badly formated code pass the CI,
so there would be no junk to reformat!
All code is perfectly formated all the time.

Rely on strict linters, not auto-formatters.
