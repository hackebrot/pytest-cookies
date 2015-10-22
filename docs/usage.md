# Usage

The ``cookies.bake()`` method generates a new project from your template based on the
default values specified in ``cookiecutter.json``:

```python
def test_bake_project(cookies):
    result = cookies.bake(extra_context={'repo_name': 'helloworld'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'helloworld'
    assert result.project.isdir()
```

It accepts the ``extra_context`` keyword argument that will be
passed to cookiecutter. The given dictionary will override the default values
of the template context, allowing you to test arbitrary user input data.

Please see the [Injecting Extra Context] section of the
official cookiecutter documentation.

  [Injecting Extra Context]: http://cookiecutter.readthedocs.org/en/latest/advanced_usage.html#injecting-extra-context
