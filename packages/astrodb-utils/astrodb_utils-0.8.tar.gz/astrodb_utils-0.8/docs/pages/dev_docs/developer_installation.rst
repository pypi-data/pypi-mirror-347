Developer Documentation
================================

Installation
---------------------

If you'd like to run tests, make sure to install the package with the optional test dependencies. E.g.,

.. code-block:: bash

    pip install -e ".[test]"

Make sure you get the `astrodb-template-db`` submodule. This is required for running tests and building the documentation.
.. code-block:: bash

    git submodule update --init --recursive


Running Tests
---------------------

All contributions should include tests. To run the tests, use the command

.. code-block:: bash

    pytest

Linting and Formatting
---------------------

Use `ruff <https://docs.astral.sh/ruff/>`_ for linting and formatting.    
A pre-commit hook is provided for automatic linting and formatting with ruff. 
To use it, run `pip install pre-commit` and then `pre-commit install --allow-missing-config`.

VSCode setup instructions: `Formatting Python in VSCode <https://code.visualstudio.com/docs/python/formatting>`_

Build the Docs
---------------------
The documentation is built using files in the `astrodb-template-db` submodule. 
Be sure to update the submodule before building the docs.
.. code-block:: bash

    git submodule update --init --recursive


To build the docs, use `sphinx-autobuild <https://pypi.org/project/sphinx-autobuild/>`_.

.. code-block:: bash

    pip install -e ".[docs]"
    sphinx-autobuild docs docs/_build/html

The docs will then be available locally at <http://127.0.0.1:8000>.
