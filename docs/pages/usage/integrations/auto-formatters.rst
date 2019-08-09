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

`autopep8 <https://github.com/hhatto/autopep8>`_ is the best choice
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

``wemake-python-styleguide`` is not compatible with ``black``.
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
