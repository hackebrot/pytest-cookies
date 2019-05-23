# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at [pytest-cookies/issues][issues].

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

[issues]: https://github.com/hackebrot/pytest-cookies/issues

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with [bug][bug] and
[help wanted][help wanted] is open to whoever wants to implement a fix for it.

[help wanted]: https://github.com/hackebrot/pytest-cookies/labels/help%20wanted
[bug]: https://github.com/hackebrot/pytest-cookies/labels/bug

### Implement Features

Look through the GitHub issues for features. Anything tagged with
[enhancement][enhancement] and [help wanted][help wanted] is open to whoever
wants to implement it.

[enhancement]: https://github.com/hackebrot/pytest-cookies/labels/enhancement
[help wanted]: https://github.com/hackebrot/pytest-cookies/labels/help%20wanted

### Write Documentation

**pytest-cookies** could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts, articles, and
such.

### Submit Feedback

The best way to send feedback is to [file an issue][issues].


If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

[issues]: https://github.com/hackebrot/pytest-cookies/issues

## Get Started!

Ready to contribute? Here's how to set up **pytest-cookies** for local
development. Please note this documentation assumes you already have
[virtualenv][virtualenv] and [git][git] installed and ready to go.

1. [Fork][fork] the **pytest-cookies** repo on GitHub.

2. Clone your fork locally:

    ```bash
    $ git clone https://github.com/YOUR-USERNAME/pytest-cookies
    ```

3. Assuming you have virtualenv installed (If you have Python3.5 this should
   already be there), you can create a new environment for your local
   development by typing:

    ``` bash
    $ python -m venv pytest-cookies-env
    $ source pytest-cookies-env/bin/activate
    ```
This should change the shell to look something like ``(pytest-cookies-env) $``

4. Create a branch for local development:

    ``` bash
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

5. Now you can make your changes locally.When you're done making changes, use
   [tox][tox] to run checks against your changes. Install it as follows:

    ``` bash
    $ pip install tox
    ```

6. First you want to make sure that your branch passes [flake8][flake8].

    ``` bash
    $ tox -e flake8
    ```

7. The next step would be to run the tests against your environment (the
   special tox environment ``py`` refers to the currently active python
   environment):

    ``` bash
    $ tox -e py
    ```

8. Before raising any pull request you should run tox. This will run the tests
   across different versions of Python:

    ``` bash
    $ tox
    ```

9. If your contribution is a bug fix or new feature, you may want to add a test
   to the existing test suite. See section *Add a New Test* below for details.

10. Commit your changes and push your branch to GitHub:

    ``` bash
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

11. Submit a pull request through the GitHub website.

[clone]: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork
[flake8]: https://pypi.python.org/pypi/flake8
[fork]: https://help.github.com/articles/fork-a-repo/
[git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[tox]: https://pypi.python.org/pypi/tox
[virtualenv]: https://virtualenv.pypa.io/en/stable/installation

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring, and add the feature to
   the list in README.md.

3. The pull request should work for Python 2.7, 3.4 and 3.5, and for PyPy.
   Check [travis pull requests][travis] and make sure that the tests pass for
   all supported Python versions.

[travis]: https://travis-ci.org/hackebrot/pytest-cookies/pull_requests

Add a New Test
---------------

When fixing a bug or adding features, it's good practice to add a test to
demonstrate your fix or new feature behaves as expected. These tests should
focus on one tiny bit of functionality and prove changes are correct.

To write and run your new test, follow these steps:

1. Add the new test to ``tests/test_<file>.py``. Focus your test on the
   specific bug or a small part of the new feature.

2. If you have already made changes to the code, stash your changes and confirm
   all your changes were stashed:

    ``` bash
    $ git stash
    $ git stash list
    ```

3. Run your test and confirm that your test fails. If your test does not fail,
   rewrite the test until it fails on the original code:

    ``` bash
    $ tox -e py
    ```

4. (Optional) Run the tests with tox to ensure that the code changes work with
   different Python versions:

    ``` bash
    $ tox
    ```

5. Proceed work on your bug fix or new feature or restore your changes. To
   restore your stashed changes and confirm their restoration:

    ``` bash
    $ git stash pop
    $ git stash list
    ```

6. Rerun your test and confirm that your test passes. If it passes,
   congratulations!

[bug]: https://github.com/hackebrot/pytest-cookies/labels/bug
[enhancement]: https://github.com/hackebrot/pytest-cookies/labels/enhancement
[help wanted]: https://github.com/hackebrot/pytest-cookies/labels/help%20wanted
[issues]: https://github.com/hackebrot/pytest-cookies/issues
