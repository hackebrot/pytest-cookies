# Installation

**pytest-cookies** is available for download from [PyPI] via [pip]:

```no-highlight
$ pip install pytest-cookies
```

It will automatically install [pytest] along with [cookiecutter].

  [PyPI]: https://pypi.python.org/pypi
  [cookiecutter]: https://github.com/cookiecutter/cookiecutter
  [pip]: https://pypi.python.org/pypi/pip/
  [pytest]: https://github.com/pytest-dev/pytest

# Usage

The ``cookies.bake()`` method generates a new project from your template based on the
default values specified in ``cookiecutter.json``:

```python
def test_bake_project(cookies):
    result = cookies.bake(extra_context={'repo_name': 'helloworld'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "helloworld"
    assert result.project_path.is_dir()
```

It accepts the ``extra_context`` keyword argument that will be
passed to cookiecutter. The given dictionary will override the default values
of the template context, allowing you to test arbitrary user input data.

Please see the [Injecting Extra Context] section of the
official cookiecutter documentation.

  [Injecting Extra Context]: https://cookiecutter.readthedocs.io/en/latest/advanced/injecting_context.html#injecting-extra-context
