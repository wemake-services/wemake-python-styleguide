PyCharm
-------

There are three ways to use ``wemake-python-styleguide`` inside
`PyCharm <https://www.jetbrains.com/pycharm/>`_:

1. `Flake8 Support plugin <https://plugins.jetbrains.com/plugin/11563-flake8-support>`_
2. A custom **File Watcher** configured to run ``flake8`` with WPS enabled
3. An **LSP server** via ``python-lsp-server`` (requires `LSP4IJ <https://plugins.jetbrains.com/plugin/23257-lsp4ij>`__)

The File Watcher approach is useful
when you want real-time feedback on every file save
or when the plugin does not pick up your WPS installation.
The LSP approach provides the richest IDE integration
with inline diagnostics, hover tooltips, and quick fixes.

Prerequisites
~~~~~~~~~~~~~

Make sure you have ``wemake-python-styleguide`` installed.
We recommend using `uv <https://docs.astral.sh/uv/>`_:

.. code:: bash

  uv tool install --with-executables-from flake8 wemake-python-styleguide

After installation the ``flake8`` binary is available on your ``PATH``
(usually at ``~/.local/bin/flake8`` on Linux and macOS).

Setting up a File Watcher
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open **Settings** (or **Preferences** on macOS).
2. Navigate to **Tools → File Watchers**.
3. Click **+** and choose **<custom>**.
4. Configure the watcher:

   - **Name**: ``wemake-python-styleguide``
   - **File type**: ``Python``
   - **Scope**: ``Project Files``
   - **Program**: ``flake8`` (or the full path from above)
   - **Arguments**: ``--select=WPS $FilePath$``
   - **Output paths to refresh**: ``$FilePath$``
   - **Working directory**: ``$ProjectFileDir$``

5. In the **Advanced Options** section enable:

   - **Auto-save edited files to trigger the watcher**
   - **Trigger the watcher on external changes**

6. Click **OK**.

The watcher will run WPS on every save and show violations
directly in the PyCharm editor and in the **Inspections** panel.

Setting up an LSP server
~~~~~~~~~~~~~~~~~~~~~~~~

This method uses ``python-lsp-server`` together with the LSP4IJ plugin
to provide inline error highlighting, hover information, and more.

1. **Install the LSP4IJ plugin**

   Go to **Settings → Plugins → Marketplace**, search for
   `LSP4IJ <https://plugins.jetbrains.com/plugin/23257-lsp4ij>`__
   and install it.

2. **Install ``python-lsp-server``**

   We recommend using `uv <https://docs.astral.sh/uv/>`_:

   .. code:: bash

     uv tool install \
       --with flake8 \
       --with wemake-python-styleguide \
       --with pyls-flake8 \
       python-lsp-server

   After installation the ``pylsp`` binary is available on your ``PATH``
   (usually at ``~/.local/bin/pylsp`` on Linux and macOS).

3. **Find the ``pylsp`` executable**

   Run ``where pylsp`` (or ``which pylsp``) and note the full path.

4. **Create a new LSP server definition**

   1. Open **Settings → Languages & Frameworks →
      Language Server Protocol → Server Definitions**.
   2. Click **+** to add a new server.
   3. Set **Name** to ``pylsp-wps`` and **Path**
      to the ``pylsp`` executable from step 3.
   4. Switch to the **Configuration** tab and paste:

      .. code:: json

        {
          "pylsp": {
            "plugins": {
              "flake8": {
                "enabled": true,
                "select": ["WPS", "E"]
              },
              "pycodestyle": { "enabled": false },
              "pyflakes": { "enabled": false },
              "mccabe": { "enabled": false }
            }
          }
        }

   5. In **Mappings** add ``Python`` as the language for this server.
   6. Click **OK**.

5. **Restart PyCharm**

   Restart the IDE completely so the LSP server can initialise.

6. **Verify**

   Open a Python file and introduce an intentional WPS violation.
   You should see inline squiggles and hover tooltips
   with the violation message.

Troubleshooting
~~~~~~~~~~~~~~~

If you do not see any violations:

- Make sure the **Program** path points to the ``flake8`` binary
  that has ``wemake-python-styleguide`` installed inside the same environment.
- Try running the same command from the terminal to verify it works.
- Check that your project has a valid ``setup.cfg`` or ``pyproject.toml``
  with WPS configuration.
