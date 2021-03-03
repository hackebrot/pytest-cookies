# Bake Result

``cookies.bake()`` returns a result instance with a bunch of fields that
hold useful information:

* ``exit_code``: is the exit code of cookiecutter, ``0`` means successful termination
* ``exception``: is the exception that happened if one did
* ``project``: a [Path] object pointing to the rendered project
* ``context``: is the rendered context

The returned ``PosixPath`` or ``WindowsPath`` instance (depending on your OS)
provides you with a powerful interface to filesystem related information that
comes in handy for validating the generated project layout and even file
contents:

```python
def test_readme(cookies):
    result = cookies.bake()

    readme_file = result.project.joinpath('README.rst')
    readme_lines = readme_file.open(newline=None)
    assert readme_lines == ['helloworld', '==========']
```

[Path]: https://docs.python.org/3/library/pathlib.html#pathlib.Path
