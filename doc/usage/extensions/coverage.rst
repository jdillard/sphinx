:mod:`sphinx.ext.coverage` -- Collect doc coverage stats
========================================================

.. module:: sphinx.ext.coverage
   :synopsis: Check Python modules and C API for coverage in the documentation.

.. role:: code-py(code)
   :language: Python

This extension measures how much of your Python or C API is included in your
documentation. It does **not** measure code coverage from tests.

For Python APIs, the coverage builder imports the configured modules, finds
public functions, classes, and methods, and compares them with the Python
objects described in the documentation. An object counts as documented when
it is described by a Python domain directive, such as :rst:dir:`py:function`,
or by an :mod:`~sphinx.ext.autodoc` directive. A docstring in the source code
alone does not count as documentation.

For C APIs, the builder searches configured C source files for API elements
and compares them with objects described by :doc:`C domain </usage/domains/c>`
directives.


Getting started
---------------

Add :mod:`sphinx.ext.coverage` to the :confval:`extensions` list in
:file:`conf.py`. For the most complete Python coverage report, also specify
the packages or modules to inspect with :confval:`coverage_modules`:

.. code-block:: python

   extensions = [
       ...
       'sphinx.ext.coverage',
   ]

   coverage_modules = ['my_package']

The coverage builder imports the modules it checks, so the package must be
installed in the build environment or otherwise available on :data:`sys.path`.

Run the coverage builder:

.. code-block:: console

   $ sphinx-build -M coverage docs docs/_build

With this example command, the Python report is written to
:file:`docs/_build/coverage/python.txt`. It contains coverage statistics and
lists the functions, classes, and methods that are not described in the
documentation. For example:

.. code-block:: text

   Undocumented Python objects
   ===========================

   Statistics
   ----------

   +--------------------+----------+--------------+
   | Module             | Coverage | Undocumented |
   +====================+==========+==============+
   | my_package.widgets | 50.00%   | 2            |
   +--------------------+----------+--------------+

   my_package.widgets
   ------------------
   Functions:
    * parse

   Classes:
    * Widget -- missing methods:

      - render

The C API report is written to :file:`c.txt` in the same directory. C API
coverage requires additional configuration with :confval:`coverage_c_path`
and :confval:`coverage_c_regexes`.

.. note::

   The :doc:`sphinx-apidoc </man/sphinx-apidoc>` command can be used to
   automatically generate API documentation for all code in a project,
   avoiding the need to manually author these documents and keep them up-to-date.

.. warning::

   :mod:`~sphinx.ext.coverage` **imports** the modules to be documented.
   If any modules have side effects on import,
   these will be executed by the coverage builder when ``sphinx-build`` is run.

   If you document scripts (as opposed to library modules),
   make sure their main routine is protected by a
   ``if __name__ == '__main__'`` condition.

.. note::

   For Sphinx (actually, the Python interpreter that executes Sphinx)
   to find your module, it must be importable.
   That means that the module or the package must be in
   one of the directories on :data:`sys.path` -- adapt your :data:`sys.path`
   in the configuration file accordingly.

If :confval:`coverage_modules` is not set, the builder checks only Python
modules already named in the documentation by an :rst:dir:`py:module` or
:rst:dir:`automodule` directive. Set :confval:`coverage_modules` to also find
packages and modules that are missing from the documentation entirely.


Builder
-------

.. py:class:: CoverageBuilder

   Checks API documentation coverage and writes plain-text reports for Python
   and C API elements.


Configuration
-------------

Several configuration values can be used to specify
what the builder should check:

.. confval:: coverage_modules
   :type: :code-py:`Sequence[str]`
   :default: :code-py:`()`

   List of Python packages or modules to test coverage for.
   When this is provided, Sphinx will introspect each package
   or module provided in this list as well
   as all sub-packages and sub-modules found in each.
   When this is not provided, Sphinx will only provide coverage
   for Python packages and modules that it is aware of:
   that is, any modules documented using the :rst:dir:`py:module` directive
   provided in the :doc:`Python domain </usage/domains/python>`
   or the :rst:dir:`automodule` directive provided by the
   :mod:`~sphinx.ext.autodoc` extension.

   .. versionadded:: 7.4

.. confval:: coverage_ignore_modules
             coverage_ignore_functions
             coverage_ignore_classes
             coverage_ignore_pyobjects
   :type: :code-py:`Sequence[str]`
   :default: :code-py:`()`

   List of `Python regular expressions`_.

   If any of these regular expressions matches any part of the full import path
   of a Python object, that Python object is excluded from the documentation
   coverage report.

   .. _Python regular expressions: https://docs.python.org/library/re

   .. versionadded:: 2.1

.. confval:: coverage_c_path
   :type: :code-py:`Sequence[str]`
   :default: :code-py:`()`

.. confval:: coverage_c_regexes
   :type: :code-py:`dict[str, str]`
   :default: :code-py:`{}`

.. confval:: coverage_ignore_c_items
   :type: :code-py:`dict[str, Sequence[str]]`
   :default: :code-py:`{}`

.. confval:: coverage_write_headline
   :type: :code-py:`bool`
   :default: :code-py:`True`

   Set to ``False`` to not write headlines.

   .. versionadded:: 1.1

.. confval:: coverage_skip_undoc_in_source
   :type: :code-py:`bool`
   :default: :code-py:`False`

   Skip objects that are not documented in the source with a docstring.

   .. versionadded:: 1.1

.. confval:: coverage_show_missing_items
   :type: :code-py:`bool`
   :default: :code-py:`False`

   Print objects that are missing to standard output also.

   .. versionadded:: 3.1

.. confval:: coverage_statistics_to_report
   :type: :code-py:`bool`
   :default: :code-py:`True`

   Print a tabular report of the coverage statistics to the coverage report.

   Example output:

   .. code-block:: text

      +-----------------------+----------+--------------+
      | Module                | Coverage | Undocumented |
      +=======================+==========+==============+
      | package.foo_module    | 100.00%  | 0            |
      +-----------------------+----------+--------------+
      | package.bar_module    | 83.33%   | 1            |
      +-----------------------+----------+--------------+

   .. versionadded:: 7.2

.. confval:: coverage_statistics_to_stdout
   :type: :code-py:`bool`
   :default: :code-py:`False`

   Print a tabular report of the coverage statistics to standard output.

   Example output:

   .. code-block:: text

      +-----------------------+----------+--------------+
      | Module                | Coverage | Undocumented |
      +=======================+==========+==============+
      | package.foo_module    | 100.00%  | 0            |
      +-----------------------+----------+--------------+
      | package.bar_module    | 83.33%   | 1            |
      +-----------------------+----------+--------------+

   .. versionadded:: 7.2
