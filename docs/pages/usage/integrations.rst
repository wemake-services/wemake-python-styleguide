Integrations
============

We leverage all the existing ``flake8``
`infrastructure <https://github.com/DmytroLitvinov/awesome-flake8-extensions>`_
and tools.
There are different integrations for your workflow.


Hooks
-----

- `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ to run style checks
  alongside with tests
- `pre-commit <https://pre-commit.com/>`_ to run ``flake8``
  before all commits locally
- `pronto-flake8 <https://github.com/scoremedia/pronto-flake8>`_ to post
  inline-comments with violations during code-review inside your CI


Editors
-------

Note, that some editors might need to disable our own :ref:`formatter`
and set the `default formatter <https://flake8.pycqa.org/en/latest/internal/formatters.html>`_
with ``format = default`` in your configuration.

- `vscode plugin <https://code.visualstudio.com/docs/python/linting>`_
- `sublime plugin <https://github.com/SublimeLinter/SublimeLinter-flake8>`_
- `atom plugin <https://atom.io/packages/linter-flake8>`_
- `vim plugin <https://github.com/nvie/vim-flake8>`_
- `emacs plugin <https://github.com/flycheck/flycheck>`_
- `pycharm plugin <https://plugins.jetbrains.com/plugin/11563-flake8-support>`_
- `wing plugin <https://github.com/grahamu/flake8panel>`_


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


Auto-formatters
---------------

Autoformatters are very simple tools to do just a one thing:
reformat some basic stuff in your code like quotes, commas, and line length.

The difference between a linter and auto-formatter is huge:

- auto-formatters pretties your code a little bit
- linters force you to write beautiful and correct code

For example, auto-formatters won't tell you that your code is too complex.
When your linter will (in case it is a good linter).

Autoformatters are also useless
when dealing with rewriting actually bad code.
Like code with bad variable names, unreachable branches,
statements that have no effect.

We in ``wemake.services`` believe that these kind of tools are not required,
because a good linter will just not let your badly formated code pass the CI,
so there would be no junk to reformat!
All code is perfectly formated all the time.

Rely on strict linters, not auto-formatters.

However, if you still want to use some autoformatter
together with ``wemake-python-styleguide``
we have made some reasearch to help you!

autopep8
~~~~~~~~

`autopep8 <https://github.com/google/yapf>`_ is the best choice
for ``wemake-python-styleguide`` users.

Is officially supported in way
that all code written inside ``wemake-python-styleguide`` is tested
to be valid ``autopep8`` code. But, **not the other way around**.

Since ``wemake-python-styleguide`` is the strictest linter
it cannot be pleased by outputs of ``autopep8`` in 100% of cases all by itself.
Most likely, you will need to refactor a little bit more manually (brainly!)
to please ``wemake-python-styleguide`` after ``autopep8`` formatting is done.

There are also plugins for IDEs to run ``autopep8`` on safe:

- https://code.visualstudio.com/docs/python/editing

isort
~~~~~

``isort`` is a great tool to sort your imports.
We already use it to validate that your imports are correct.
We recommend to use ``isort`` and officially
and support it in a way that all
valid ``wemake-python-styleguide`` code is valid ``isort`` code.
But, **not the other way around**.

You might be required to refactor your code manually after ``isort``
reformat to make ``wemake-python-styleguide`` happy.

``isort`` can also `be invoked <https://github.com/timothycrosley/isort#using-isort>`_
as a command line tool to fix all your import problems for you.

We recommend to run ``isort`` after ``autopep8``. They are also compatible.

There are also plugins for IDEs to run ``isort`` on safe:

- https://github.com/timothycrosley/isort/wiki/isort-Plugins
- https://code.visualstudio.com/docs/python/editing

You can find the configuration we use in ``setup.cfg`` in this repository.

yapf
~~~~

This a very complex autoformatter written by Google.
It has like lots of configuration options!

We were not successful enough to configure it
in a way that our style is respected.
The main problems are with new lines and trailing commas:
sometimes they are added, sometimes removed.

If you have a working configuration
for both ``yapf`` and ``wemake-python-styleguide``,
please, let us know!

black
~~~~~

``wemake-python-styleguide`` is not compatible to ``black``.
Let's go deeper and see why.

``black`` itself is actually not compatible with ``PEP8`` and ``flake8``
(`docs <https://black.readthedocs.io/en/stable/the_black_code_style.html?highlight=flake8>`_),
that's why it is not compatible with ``wemake-python-styleguide`` either.
Here are the violations that ``black`` produces:

- Quotes: for some reasons ``black`` uses ``"``
  that almost no one uses in the ``python`` world
- Trailing commas: ``black`` strips trailing commas and this makes
  adding new code harder to review, since your ``git diff`` is poluted
  by a comma change, the sad thing that tailing commas as a best-practice
  are quite popular in ``python`` code
- Line length. Violating rules by 10%-15% is not ok.
  You either violate them or not. ``black`` violates line-length rules.

And there's no configuration to fix it!
Shame, that official ``python-org`` product violates the community standards
and not enforcing them.
