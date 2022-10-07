.. _legacy:

Legacy projects
---------------

Introducing this package to a legacy project is going to be a challenge.
Due to our strict quality, consistency, and complexity rules.

But, you still can do several things to integrate this linter step by step:

1. Fix consistency, naming and best-practices violations,
   they are the easiest to clean up.
2. Per-file ignore complexity checks that are failing for your project.
   Sometimes it is possible to rewrite several parts of your code,
   but generally complexity rules are the hardest to fix.
3. Use `boy scout rule <https://deviq.com/principles/boy-scout-rule>`_: always leave
   your code better than you found it.

To make sure "boy scout rule" works we officially support ``--diff`` mode.
The main idea of it is simple: we only lint things that we touch.

We also support :ref:`flakeheaven-legacy` (external tool)
to create a ``baseline`` of your current violations
and start to lint only new one from this point.

Choose what suits you best.

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

Of course, it won't make its way through our linter.
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

.. rubric:: Further reading

- :ref:`Creating baselines for legacy projects <flakeheaven>`
