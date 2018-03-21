# Bake Result

``cookies.bake()`` returns a result instance with a bunch of fields that
hold useful information:

* ``exit_code``: is the exit code of cookiecutter, ``0`` means successful termination
* ``exception``: is the exception that happened if one did
* ``project``: a [py.path.local] object pointing to the rendered project
* ``trace_back`` : a trace back object associated with the ``exception``
  (if an exception happend, ``None`` otherwise)

The result instance also has a helper property that will turn the trace_back
object into a stack trace string:

```python
    result = cookies.bake()

    if result.trace_back:
        print(result.trace_back_stack)
```

The returned ``LocalPath`` instance provides you with a powerful interface
to filesystem related information, that comes in handy for validating the generated
project layout and even file contents:

```python
def test_readme(cookies):
    result = cookies.bake()

    readme_file = result.project.join('README.rst')
    readme_lines = readme_file.readlines(cr=False)
    assert readme_lines == ['helloworld', '==========']
```
  [py.path.local]: http://pylib.readthedocs.org/en/latest/path.html#py._path.local.LocalPath
