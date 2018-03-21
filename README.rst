Pytest-Cookies
==============

|gitter| |pypi| |pyversions| |license| |rtfd| |travis-ci| |appveyor|

`pytest`_ is a mature full-featured Python testing tool that provides easy,
no boilerplate testing. Its hook-based customization system supports integration
of external plugins such as **pytest-cookies**.

This plugin comes with a ``cookies`` fixture which is a wrapper for the
`cookiecutter`_ API for generating projects. It helps you verify that your
template is working as expected and takes care of cleaning up after running the
tests.

|cookiecutter|

Installation
------------

**pytest-cookies** is available for download from `PyPI`_ via `pip`_::

    $ pip install pytest-cookies

It will automatically install `pytest`_ along with `cookiecutter`_.

Features
--------

``cookies.bake()`` returns a result instance with a bunch of fields that hold
useful information:

* ``exit_code``: is the exit code of cookiecutter, ``0`` means successful
  termination
* ``exception``: is the exception that happened (if one did, ``None``
  otherwise)
* ``project``: a `py.path.local`_ object pointing to the rendered project

The returned ``LocalPath`` instance provides you with a powerful interface to
filesystem related information, that comes in handy for validating the
generated project layout and file contents:

.. code-block:: python

    def test_readme(cookies):
        result = cookies.bake()

        readme_file = result.project.join('README.rst')
        readme_lines = readme_file.readlines(cr=False)

        assert readme_lines == [
            'helloworld',
            '==========',
        ]

Usage
-----

Generate a new project
~~~~~~~~~~~~~~~~~~~~~~

The ``cookies.bake()`` method generates a new project from your template based on the
default values specified in ``cookiecutter.json``:

.. code-block:: python

    def test_bake_project(cookies):
        result = cookies.bake(extra_context={'repo_name': 'helloworld'})

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == 'helloworld'
        assert result.project.isdir()

It accepts the ``extra_context`` keyword argument that will be
passed to cookiecutter. The given dictionary will override the default values
of the template context, allowing you to test arbitrary user input data.

Please see the `Injecting Extra Context`_ section of the
official cookiecutter documentation.

Specify template directory
~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``cookies.bake`` looks for a `cookiecutter`_ template in the
current directory. This can be overridden on the command line by passing a
``--template`` parameter to `pytest`_:

.. code-block::

    $ pytest --template TEMPLATE

To customize the `cookiecutter`_ template directory in a test,
``cookies.bake()`` can also accept an optional ``template`` parameter:

.. code-block:: python

    @pytest.fixture
    def custom_template(tmpdir):
        template = tmpdir.ensure('cookiecutter-template', dir=True)
        template.join('cookiecutter.json').write(
            '{"repo_name": "example-project"}'
        )

        repo_dir = template.ensure('{{cookiecutter.repo_name}}', dir=True)
        repo_dir.join('README.rst').write('{{cookiecutter.repo_name}}')

        return template


    def test_bake_custom_project(cookies, custom_template):
        """Test for 'cookiecutter-template'."""
        result = cookies.bake(template=str(custom_template))

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == 'example-project'
        assert result.project.isdir()

Keep Output Directories for Debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the ``cookies`` fixture will remove all baked projects.
However, you can pass the flag ``keep-baked-projects`` if you'd like
to keep them (`it won't clutter`_, pytest will remove entries older than 3
temporary directories):

.. code-block::

    $ pytest --keep-baked-projects

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed
description.

Contributing
------------

Contributions are very welcome! Tests can be run with `tox`_, please make sure
all of the tests are green before you submit a pull request.

Code of Conduct
---------------

Everyone interacting in the **pytest-cookies** project's codebases, issue
trackers, chat rooms, and mailing lists is expected to follow the `PyPA Code of
Conduct`_.

License
-------

Distributed under the terms of the `MIT`_ license, Pytest-Cookies is free and
open source software.

.. image:: https://opensource.org/trademarks/osi-certified/web/osi-certified-120x100.png
   :align: left
   :alt: OSI certified
   :target: https://opensource.org/

.. _`it won't clutter`: https://docs.pytest.org/en/latest/tmpdir.html#the-default-base-temporary-directory
.. _`cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/hackebrot/pytest-cookies/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`Injecting Extra Context`: http://cookiecutter.readthedocs.io/en/latest/advanced/injecting_content.html
.. _`py.path.local`: http://py.readthedocs.io/en/latest/path.html#py._path.local.LocalPath
.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/

.. |gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/hackebrot/pytest-cookies
   :target: https://gitter.im/hackebrot/pytest-cookies?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |pypi| image:: https://img.shields.io/pypi/v/pytest-cookies.svg
   :target: https://pypi.python.org/pypi/pytest-cookies
   :alt: PyPI Package

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pytest-cookies.svg
   :target: https://pypi.python.org/pypi/pytest-cookies/
   :alt: PyPI Python Versions

.. |license| image:: https://img.shields.io/pypi/l/pytest-cookies.svg
   :target: https://pypi.python.org/pypi/pytest-cookies
   :alt: PyPI Package License

.. |rtfd| image:: https://readthedocs.org/projects/pytest-cookies/badge/?version=latest
    :target: http://pytest-cookies.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. |travis-ci| image:: https://travis-ci.org/hackebrot/pytest-cookies.svg?branch=master
    :target: https://travis-ci.org/hackebrot/pytest-cookies
    :alt: See Build Status on Travis CI

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/hackebrot/pytest-cookies?branch=master
    :target: https://ci.appveyor.com/project/hackebrot/pytest-cookies/branch/master
    :alt: See Build Status on AppVeyor

.. |cookiecutter| image:: https://raw.github.com/audreyr/cookiecutter/aa309b73bdc974788ba265d843a65bb94c2e608e/cookiecutter_medium.png
    :target: https://github.com/audreyr/cookiecutter
    :alt: Cookiecutter
