.. _tutorial:

Tutorial
========

When you want to force someone to write the code the way you want:
you need to create a :term:`rule` for that.

There are multiple options of how this can be done.
This guide will walk trough all possible cases and cover every decision path.

Deciding what exactly to write
------------------------------

The most important thing is the question:
what kind of rule do you want to create?

Depending on the answer you can end up with either:

1. Creating a new ``flake8`` :term:`plugin`
2. Creating a pair of new :term:`visitor` and :term:`violation`
   inside this plugin, and some checking logic to find problems with your code
3. Just a new :term:`violation` and checking logic to find
   problems with your code

What does it depend on internally?

Writing new plugin
------------------

First of all, you have to decide:

1. Are you writing a separate plugin and adding it as a dependency?
2. Are you writing a built-in extension to this styleguide?

How to make a decision?

Will this plugin be useful to other developers without this styleguide?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If so, it would be wise to create a separate ``flake8`` plugin.
Then you can add newly created plugin as a dependency.
Our rules do not make any sense without each other.

It is also useful when you try to wrap an existing tool into ``flake8`` API.

Real world examples of tools that are useful by them self:

- `flake8-eradicate <https://github.com/sobolevn/flake8-eradicate>`_
- `flake8-type-annotations <https://github.com/sobolevn/flake8-type-annotations>`_

Can this plugin be used with the existing checker?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``flake8`` has a very strict API about plugins.
Here are some problems that you may encounter:

- Some plugins are called once per file, some are called once per line
- Plugins should define clear ``violation code`` / ``checker`` relation
- It is impossible to use the same letter violation codes for several checkers

So, if you want a plugin to work with
each logical line - you have to create a custom :term:`plugin`.

Real world examples of plugins unsuitable for this checker:

- `flake8-broken-line <https://github.com/sobolevn/flake8-broken-line>`_

Is this rule out off scope?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are awesome tools that cannot be added
because they are just simply out of scope.
This means that they cover very specific case or technology
and not just good-old ``python``.

Real world examples of plugins that are out of scope:

- `flake8-pytest-style <https://github.com/m-burst/flake8-pytest-style>`_
- `flake8-django <https://github.com/rocioar/flake8-django>`_
- `flake8-scrapy <https://github.com/stummjr/flake8-scrapy>`_

All these plugins should be installed
individually to the end-user dependencies. And only when user really want it.
So, it is up to the user to decide.

And these plugins while being awesome won't be added to our project at all.

Conclusion
~~~~~~~~~~

If you said "yes" to any of these question - write a :term:`plugin`.
Then possibly add it as a dependency to this project.


Writing new visitor
-------------------

If you are still willing to write a builtin extension to this project,
you will have to write a :ref:`violation <violations>`
and/or :ref:`visitor <visitors>`.

First of all, you have to decide what base class do you want to use?

There are several possibilities:

.. autoclasstree:: wemake_python_styleguide.visitors.base

When to choose what base class?
Imagine that you have several ideas in mind:

1. I want to lint module names not to contain numbers
2. I want to lint code not to contain number ``3``
3. I want to lint code to disallow multiplication of exactly two number

Each of these tasks will require different approaches.

1. Will require to subclass a filename-based visitor
2. Will require to subclass a ``tokenize``-based visitor
3. Will require to subclass a ``ast``-based visitor

How to differ these cases by yourself?

1. You need to read though the :ref:`docs <contributing>`
   of ``ast`` and ``tokenize`` modules
2. You can have a look at the existing visitors

But, you might not want to write a new visitor.
You can reuse existing ones and write only a violation and checking logic.

Technical documentation about the :ref:`visitors` is available.


Writing new violation
---------------------

The only thing you should care about is to select
the correct base class for new violation.

.. autoclasstree:: wemake_python_styleguide.violations.base

It only depends on already selected visitor type,
so you won't have to make this decision twice.

Technical documentation about the :ref:`violations` is available.


Writing business logic
----------------------

When you will have your :term:`visitor` and :term:`violation`
it will be required to actually write
some logic to raise a ``violation`` from ``visitor``.

We do this inside the ``visitor``,
but we create protected methods and place logic there.

Consider this example:

.. code:: python

  class WrongComprehensionVisitor(BaseNodeVisitor):
      _max_ifs = 1

      def _check_ifs(self, node: ast.comprehension) -> None:
          if len(node.ifs) > self._max_ifs:
              # This will restrict to have more than 1 `if`
              # in your comprehensions:
              self.add_violation(MultipleIfsInComprehensionViolation(node))

      def visit_comprehension(self, node: ast.comprehension) -> None:
          self._check_ifs(node)
          self.generic_visit(node)

You may also end up using the same logic over and over again.
In this case we can decouple it and move to ``logics/`` package.

Then it would be easy to reuse something.


Writing tests
-------------

Writing end-to-end tests
~~~~~~~~~~~~~~~~~~~~~~~~

In end-to-end tests we check that our visitor, violation and business logic
work correctly together all the way from flake8 config file to its output.

To check all supported violations, we have two modules containing code which
raises them: ``noqa.py`` and ``noqa_controlled.py``. The first is for all
possible violations while the second is only for those which may be tweaked
using ``i_control_code`` option. If violation may be ignored (or instead,
raised) with ``i_control_code``, the appropriate piece of code should be
added to both modules.

The next thing is test itself which should reside in
``tests/test_checker/test_noqa.py`` module. The main test functions are
written already, so probably the only thing to do is to put the violation
code into either ``SHOULD_BE_RAISED``, or ``SHOULD_BE_RAISED_NO_CONTROL``
container, or into both. For example, if the violation is raised with
``i_control_code=True``, it must be placed into ``SHOULD_BE_RAISED``
with value ``1`` and into ``SHOULD_BE_RAISED_NO_CONTROL`` with value ``0``.
By doing this we check that the violation is raised in one situation and
is not raised in opposite one. If the violation is ignored when
``i_control_code=True``, swap ``0`` and ``1`` it containers. If the
violation cannot be tweaked with ``i_control_code`` it should only be
put into ``SHOULD_BE_RAISED`` container with appropriate value.
