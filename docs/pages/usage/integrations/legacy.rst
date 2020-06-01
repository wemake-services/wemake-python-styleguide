.. _legacy:

Legacy projects
===============

Introducing this package to a legacy project is going to be a challenge.
Due to our strict quality, consistency, and complexity rules.

But, you still can do several things to integrate this linter step by step:

1. Generate a baseline to ignore existing violations
   and only report new ones that were created after the baseline.
2. Fix consistency, naming and best-practices violations,
   they are the easiest to clean up.
3. Per-file ignore complexity checks that are failing for your project.
   Sometimes it is possible to rewrite several parts of your code,
   but generally complexity rules are the hardest to fix.
4. Use `boyscout rule <https://deviq.com/boy-scout-rule/>`_: always leave
   your code better than you found it.

To make sure "boy scout rule" works we officially support ``--diff`` mode.
The main idea of it is simple: we only lint things that we touch.

Choose what suits you best.

.. _baseline:

Baseline
--------

You can start using our linter with just a single command!

.. code:: bash

  flake8 --baseline your_project

This guide will explain how it works.

Steps
~~~~~

There are several steps in how baseline works.

We can run the linter with ``--baseline`` mode enabled.
What will happen?

If you don't have ``.flake8-baseline.json``,
then a new one will be created containing all the violations you have.
The first time all violations will be reported.
We do this to show the contents of the future baseline to the developer.
Futher runs won't report any of the violations inside the baseline.

If you already have ``.flake8-baseline.json`` file,
than your baselined violations will be ignored.

However, new violations will still be reported.

Updating baseline
~~~~~~~~~~~~~~~~~

To update a baseline you can delete the old one:

.. code:: bash

  rm .flake8-baseline.json

And create a new one with ``--baseline`` flag:

.. code:: bash

  flake8 --baseline your_project

Baseline contents
~~~~~~~~~~~~~~~~~

Things we care when working with baselines:

1. Violation codes and text descriptions
2. Filenames

When these values change
(for example: file is renamed or violation code is changed),
we will treat these violations as new ones.
And report them to the user as usual.

Things we don't care when working with baselines:

1. Violation locations, because lines and columns
   can be easily changed by simple refactoring
2. Activated plugins
3. Config values
4. Target files and directories

So, when you add new plugins or change any config values,
then you might want ot update the baseline as well.

Full baseline example
~~~~~~~~~~~~~~~~~~~~~

You start with a legacy file that looks like this:

.. code:: python

  # ex.py
  x = 1

Let's lint it and ignore existing errors!

.. code:: bash

  flake8 --baseline ex.py

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/baseline-initial.png

We are seeing our violation. Works as expected.
Also, now your baseline is generated. Let's see that it works:

.. code:: bash

  cat .flake8-baseline.json

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/baseline-contents.png

Yes, here it is. It contains a single violation from your ``ex.py`` file.
Let's run ``flake8`` again to see that no violations are going
to be reported with a baseline:

.. code:: bash

  flake8 --baseline ex.py

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/baseline-existing.png

That works! No violations are reported.
Because baseline covers all existing ones.
Let's add some new ones to test that it will raise a violation:

.. code:: python

  # ex.py
  x = 1
  y = 1

And run the linter:

.. code:: bash

  flake8 --baseline ex.py

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/baseline-new-violations.png

And yes, new violation is reported! It works just as we planned.
Enjoy your incremental adoption!


Linting diffs
-------------

Existing legacy
~~~~~~~~~~~~~~~

You can also use `--diff option <http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-diff>`_
of ``flake8`` to lint the latest changes only.

This mode is officially supported and fully-operational.

Let's take a look at the example.
Imagine that we have this old and very big class (like 1000 lines of code):

.. code:: python

  class ExistingOldAndVeryBigClass:

      def method_we_do_not_care_about(self):
          return 5

      def method_we_need_to_touch(self):
          return

Of course, it won't make its way trough our linter.
And you obviously do not want to refactor 1000s lines of code
just to make a simple fix to ``method_we_need_to_touch``.

New changes to it
~~~~~~~~~~~~~~~~~

We need to do something (we don't care about the code's logic in this example)
with ``method_we_need_to_touch`` only:

.. code:: python

  class ExistingOldAndVeryBigClass:

      def method_we_do_not_care_about(self):
          return 5

      def method_we_need_to_touch(self):
          x = self.method_we_do_not_care_about()
          print(x)
          return

Changes as diff
~~~~~~~~~~~~~~~

Now, when we made the required change, let's see the diff.

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/diff.png

That's where ``--diff`` option is helpful. Let's use it!

.. code:: bash

  git diff | flake8 --diff

We use `git-diff <https://git-scm.com/docs/git-diff>`_ to show
the difference between the previous state and current changes.
But, you can use `diff <https://www.computerhope.com/unix/udiff.htm>`_
command itself or any other ``diff`` producers.

That's what is going to be reported:

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/legacy.png

See? We only count things that were changed.
And all other violations are ignored.

Fixing one thing at a time
~~~~~~~~~~~~~~~~~~~~~~~~~~

It means that we only need to fix things we have touched in this commit:

.. code:: python

  class ExistingOldAndVeryBigClass:

      def method_we_do_not_care_about(self):
          return 5

      def method_we_need_to_touch(self):
          """Do this and that."""
          value_to_log = self.method_we_do_not_care_about()
          # We really need to log it, so it will be shown in logs:
          print(value_to_log)  # noqa: WPS421

That's it. We have passed out linter with just so few refactoring.

Of course, it has a downside: the ugly code still lives with you,
but new ugly code won't make its way to the project.
And you are forced to improve things you write.

At some point in time, you will have 100% perfect code.
Good linters and constant refactoring is the key to the success.
