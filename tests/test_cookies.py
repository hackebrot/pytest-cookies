# -*- coding: utf-8 -*-

import json
import pytest


def test_cookies_fixture(pytester):
    """Make sure that pytest accepts the `cookies` fixture."""
    # create a temporary pytest test module
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_valid_fixture(cookies):
            assert hasattr(cookies, 'bake')
            assert callable(cookies.bake)
    """
    )

    # run pytest with the following cmd args
    result = pytester.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_valid_fixture PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_cookies_bake_with_template_kwarg(pytester, cookiecutter_template):
    """bake accepts a template kwarg."""
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.name == 'helloworld'
            assert result.project.is_dir()

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % cookiecutter_template
    )

    # run pytest without the template cli arg
    result = pytester.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_cookies_bake_template_kwarg_overrides_cli_option(
    pytester, cookiecutter_template
):
    """bake template kwarg overrides cli option."""
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.name == 'helloworld'
            assert result.project.is_dir()

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % cookiecutter_template
    )

    # run pytest with a bogus template name
    # it should use template directory passed to `cookies.bake`
    result = pytester.runpytest("-v", "--template=foobar")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_cookies_bake(pytester, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(extra_context={'repo_name': 'helloworld'})

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.name == 'helloworld'
            assert result.project.is_dir()

            assert str(result) == '<Result {}>'.format(result.project)
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(cookiecutter_template))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_cookies_bake_result_context(pytester, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.

    Check that the result holds the rendered context.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import collections

        def test_bake_project(cookies):
            result = cookies.bake(extra_context=collections.OrderedDict([
                ('repo_name', 'cookies'),
                ('short_description', '{{cookiecutter.repo_name}} is awesome'),
            ]))

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.name == 'cookies'
            assert result.project.is_dir()

            assert result.context == {
                'repo_name': 'cookies',
                'short_description': 'cookies is awesome',
            }

            assert str(result) == '<Result {}>'.format(result.project)
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(cookiecutter_template))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_cookies_bake_result_context_exception(pytester, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.

    Check that exceptions resulting from rendering the context are stored on
    result and that the rendered context is not set.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import collections

        def test_bake_project(cookies):
            result = cookies.bake(extra_context=collections.OrderedDict([
                ('repo_name', 'cookies'),
                ('short_description', '{{cookiecutter.nope}}'),
            ]))

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None

            assert result.context is None

            assert str(result) == '<Result {!r}>'.format(result.exception)
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(cookiecutter_template))

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])


def test_cookies_bake_should_create_new_output_directories(
    pytester, cookiecutter_template
):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_should_create_new_output(cookies):
            first_result = cookies.bake()
            assert first_result.exception is None
            assert str(first_result.project.parent).endswith('bake00')

            second_result = cookies.bake()
            assert second_result.exception is None
            assert str(second_result.project.parent).endswith('bake01')
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(cookiecutter_template))

    result.stdout.fnmatch_lines(["*::test_bake_should_create_new_output PASSED*"])


def test_cookies_fixture_removes_output_directories(pytester, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-
        from pathlib import Path

        def test_to_create_result(cookies):
            global result_path
            result = cookies.bake()
            result_path = result.project
            assert result.exception is None

        def test_previously_generated_directory_is_removed(cookies):
            exists = result_path.is_dir()
            assert exists is False
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(cookiecutter_template))

    result.stdout.fnmatch_lines(
        [
            "*::test_to_create_result PASSED*",
            "*::test_previously_generated_directory_is_removed PASSED*",
        ]
    )


def test_cookies_fixture_doesnt_remove_output_directories(
    pytester, cookiecutter_template
):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-
        from pathlib import Path

        def test_to_create_result(cookies):
            global result_path
            result = cookies.bake()
            result_path = result.project
            assert result.exception is None

        def test_previously_generated_directory_is_not_removed(cookies):
            exists = result_path.is_dir()
            assert exists is True
    """
    )

    result = pytester.runpytest(
        "-v", "--template={}".format(cookiecutter_template), "--keep-baked-projects"
    )

    result.stdout.fnmatch_lines(
        [
            "*::test_to_create_result PASSED*",
            "*::test_previously_generated_directory_is_not_removed PASSED*",
        ]
    )


def test_cookies_bake_should_handle_exception(pytester):
    """Programmatically create a **Cookiecutter** template and make sure that
    cookies.bake() handles exceptions that happen during project generation.

    We expect **Cookiecutter** to raise a `NonTemplatedInputDirException`.
    """
    template = pytester.path.joinpath("cookiecutter-fail")
    template.mkdir(exist_ok=True)

    template_config = {"repo_name": "foobar", "short_description": "Test Project"}
    template.joinpath("cookiecutter.json").write_text(json.dumps(template_config))

    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_should_fail(cookies):
            result = cookies.bake()

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None
    """
    )

    result = pytester.runpytest("-v", "--template={}".format(template))

    result.stdout.fnmatch_lines(["*::test_bake_should_fail PASSED*"])


@pytest.mark.parametrize("choice", ["mkdocs", "sphinx", "none"])
def test_cookies_bake_choices(pytester, choice):
    """Programmatically create a **Cookiecutter** template and make sure that
    cookies.bake() works with choice variables.
    """
    template = pytester.path.joinpath("cookiecutter-choices")
    template.mkdir(exist_ok=True)

    template_config = {"repo_name": "docs", "docs_tool": ["mkdocs", "sphinx", "none"]}
    template.joinpath("cookiecutter.json").write_text(json.dumps(template_config))

    repo = template.joinpath("{{cookiecutter.repo_name}}")
    repo.mkdir(exist_ok=True)
    repo.joinpath("README.rst").write_text("docs_tool: {{cookiecutter.docs_tool}}")

    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'docs_tool': '%s'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.name == 'docs'
            assert result.project.is_dir()

            assert result.project.joinpath('README.rst').read_text() == 'docs_tool: %s'

            assert str(result) == '<Result {}>'.format(result.project)
    """
        % (choice, template, choice)
    )

    # run pytest without the template cli arg
    result = pytester.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_bake_project PASSED*"])

    result = pytester.runpytest("-v", "--template={}".format(template))
