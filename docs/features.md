# Features

## Bake Results

``cookies.bake()`` returns a result instance with a bunch of fields that
hold useful information:

* ``exit_code``: is the exit code of cookiecutter, ``0`` means successful termination
* ``exception``: is the exception that happened if one did
* ``project_path``: a [Path] object pointing to the rendered project
* ``context``: is the rendered context

The [Path] instance in `project_path` provides you with a powerful interface to
filesystem related information, that comes in handy for validating the generated
project layout and even file contents:

```python
def test_readme(cookies):
    result = cookies.bake()

    readme_file = result.project_path / "README.rst"
    readme_lines = readme_file.read_text().splitlines()

    assert readme_lines == ["helloworld", "=========="]
```

## Cookies Session
``cookies_session`` is the same as `cookies` but the instance uses the ["session" scope].

This is useful when you want to run multiple tests on the same cookiecutter instance without having to setup and teardown with each test.

```python
    @pytest.fixture(scope="module")
    def bakery(cookies_session):
        """create a session-wide cookiecutter instance"""
        result = cookies_session.bake(extra_context={
            "value_1": "value_1",
            "value_2": "value_2",
        })
        yield result

    def test_session_project_path(bakery):
        """The first test checks for value 1"""
        assert bakery.context["value_1"] == "value_1"

    def test_session_same_project_path(bakery):
        """The second test checks for value 2"""
        assert bakery.context["value_2"] == "value_2"
```

[path]: https://docs.python.org/3/library/pathlib.html#pathlib.Path
["session" scope]: https://docs.pytest.org/en/7.1.x/how-to/fixtures.html?highlight=scope#scope-sharing-fixtures-across-classes-modules-packages-or-session
