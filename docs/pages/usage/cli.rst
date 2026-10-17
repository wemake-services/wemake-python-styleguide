Command line tool and AI
========================

CLI
---

.. versionadded:: 1.1.0

WPS has a command-line utility named ``wps``

Here are listed all the subcommands it has.

wps explain
~~~~~~~~~~~

This command can be used to get description of violation.
It will be the same description that is located on the website.

Syntax: ``wps explain <code>``

Examples:

.. code:: console

   $ wps explain WPS115
   WPS115 — Require ``snake_case`` for naming class attributes.

   Attributes in Enum and enum-like classes (Django Choices)
   are ignored, as they should be written in UPPER_SNAKE_CASE
   ...

.. code:: console

   $ wps explain 116
   WPS116 — Forbid using more than one consecutive underscore in variable names.

   Reasoning:
       This is done to gain extra readability.
   ...

AI features
-----------

.. versionadded:: 1.8.0

``wemake-python-styleguide`` supports multiple AI features
to help your agent writing the best possible Python code.

We support several different AI features for most of the agents / models.

Skill
~~~~~

Install for any harness / provider,
using `npx skills <https://github.com/vercel-labs/skills>`_:

.. code:: console

  $ npx skills add wemake-services/wemake-python-styleguide

Install with `Claude <https://code.claude.com/docs/en/discover-plugins>`_,
run inside the Claude code:

.. code:: console

  /plugin marketplace add wemake-services/wemake-python-styleguide
  /plugin install wps@wemake-python-styleguide

Or just copy `the skill file <https://github.com/wemake-services/wemake-python-styleguide/blob/master/wemake_python_styleguide/.agents/skills/wps/SKILL.md>`_.

MCP
~~~

WPS has an MCP server with one tool, ``explain_violation``.
It returns the same text as ``wps explain``.
The WPS skill above tells your agent when to call it.

Your agent starts the server from its MCP config,
for example ``.mcp.json`` in the project root for Claude Code:

.. code:: json

   {
     "mcpServers": {
       "wps": {
         "command": "uvx",
         "args": [
           "--from", "wemake-python-styleguide[mcp]",
           "python", "-m", "wemake_python_styleguide.mcp"
         ]
       }
     }
   }

Or ``pip install 'wemake-python-styleguide[mcp]'``
and replace ``command`` and ``args`` above,
using the absolute path to the Python you installed it into:

.. code:: json

   "command": "/path/to/venv/bin/python",
   "args": ["-m", "wemake_python_styleguide.mcp"]

To debug from a repository checkout, open the server in the MCP Inspector:

.. code:: console

   $ mcp dev wemake_python_styleguide/mcp.py:mcp

The server uses stdio and opens no network port.
