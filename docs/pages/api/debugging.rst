Debugging
=========

In case something does not work the way you want
there are several ways to debug things.

Viewing module contents
-----------------------

We recommend to create a simple file with just the part that does not work.
We usually call this file ``ex.py`` and remove it before the actual commit.

To reveal internals of this Python source code, you can use following options:

* ``astboom < ex.py`` will show you pretty-printed ``ast`` contents
* ``tokelor ex.py`` will show you pretty-printed token stream

It might not be enough to find some complex cases, but it helps.

Test-driven development
-----------------------

A lot of people (including @sobolevn) finds
test-driven development really useful to design and debug your code.

How?

1. Write a single test that fails for your new feature or exposes a bug
2. Run it with ``pytest tests/full/path/to/your/test_module.py``
3. Use the magic of ``print`` and ``ast.dump`` to view the contents of nodes
4. Fix the bug or implement a new feature
5. Make sure that everything works now: tests must pass
6. Done!

Interactive debugging
---------------------

We recommend to use ``ipdb`` for interactive debugging
(it is already included as a development package to this project).

To start interactive debugging session you will need to:

1. Set ``export PYTHONBREAKPOINT=ipdb.set_trace`` environment variable
2. Put ``breakpoint()`` call in places where you need your debugger to stop
3. Run your program as usual, debugger will stop on places you marked

This way allows to view local variables,
execute operations step by step, debug complex algorithms.

Visual debugging
----------------

One can use ``vscode`` or ``pycharm`` to visually debug your app.
In this case you need to setup appropriate entrypoints
and run your app in debug mode.
