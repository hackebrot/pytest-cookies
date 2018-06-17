# -*- coding: utf-8 -*-

import json
import pytest


def test_cookies_fixture(testdir):
    """Make sure that pytest accepts the `cookies` fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_valid_fixture(cookies):
            assert hasattr(cookies, 'bake')
            assert callable(cookies.bake)
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_valid_fixture PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_cookies_bake_with_template_kwarg(testdir, cookiecutter_template):
    """bake accepts a template kwarg."""
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()

            assert str(result) == '<Result {}>'.format(result.project)
    """ % cookiecutter_template)

    # run pytest without the template cli arg
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])


def test_cookies_bake_template_kwarg_overrides_cli_option(
    testdir,
    cookiecutter_template,
):
    """bake template kwarg overrides cli option."""

    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'repo_name': 'helloworld'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()

            assert str(result) == '<Result {}>'.format(result.project)
    """ % cookiecutter_template)

    # run pytest with a bogus template name
    # it should use template directory passed to `cookies.bake`
    result = testdir.runpytest('-v', '--template=foobar')

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])


def test_cookies_bake(testdir, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(extra_context={'repo_name': 'helloworld'})

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()

            assert str(result) == '<Result {}>'.format(result.project)
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template)
    )

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])


def test_cookies_bake_result_context(testdir, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.

    Check that the result holds the rendered context.
    """

    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        import collections

        def test_bake_project(cookies):
            result = cookies.bake(extra_context=collections.OrderedDict([
                ('repo_name', 'cookies'),
                ('short_description', '{{cookiecutter.repo_name}} is awesome'),
            ]))

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'cookies'
            assert result.project.isdir()

            assert result.context == {
                'repo_name': 'cookies',
                'short_description': 'cookies is awesome',
            }

            assert str(result) == '<Result {}>'.format(result.project)
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template)
    )

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])


def test_cookies_bake_result_context_exception(testdir, cookiecutter_template):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.

    Check that exceptions resulting from rendering the context are stored on
    result and that the rendered context is not set.
    """

    testdir.makepyfile("""
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
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template)
    )

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])


def test_cookies_bake_should_create_new_output_directories(
    testdir, cookiecutter_template
):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_should_create_new_output(cookies):
            first_result = cookies.bake()
            assert first_result.exception is None
            assert first_result.project.dirname.endswith('bake00')

            second_result = cookies.bake()
            assert second_result.exception is None
            assert second_result.project.dirname.endswith('bake01')
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template)
    )

    result.stdout.fnmatch_lines([
        '*::test_bake_should_create_new_output PASSED*',
    ])


def test_cookies_fixture_removes_output_directories(
    testdir, cookiecutter_template
):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-
        import os

        def test_to_create_result(cookies):
            global result_dirname
            result = cookies.bake()
            result_dirname = result.project.dirname
            assert result.exception is None

        def test_previously_generated_directory_is_removed(cookies):
            exists = os.path.isdir(result_dirname)
            assert exists is False
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template)
    )

    result.stdout.fnmatch_lines([
        '*::test_to_create_result PASSED*',
        '*::test_previously_generated_directory_is_removed PASSED*',
    ])


def test_cookies_fixture_doesnt_remove_output_directories(
    testdir, cookiecutter_template
):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    testdir.makepyfile("""
        # -*- coding: utf-8 -*-
        import os

        def test_to_create_result(cookies):
            global result_dirname
            result = cookies.bake()
            result_dirname = result.project.dirname
            assert result.exception is None

        def test_previously_generated_directory_is_not_removed(cookies):
            exists = os.path.isdir(result_dirname)
            assert exists is True
    """)

    result = testdir.runpytest(
        '-v',
        '--template={}'.format(cookiecutter_template),
        '--keep-baked-projects'
    )

    result.stdout.fnmatch_lines([
        '*::test_to_create_result PASSED*',
        '*::test_previously_generated_directory_is_not_removed PASSED*',
    ])


def test_cookies_bake_should_handle_exception(testdir):
    """Programmatically create a **Cookiecutter** template and make sure that
    cookies.bake() handles exceptions that happen during project generation.

    We expect **Cookiecutter** to raise a `NonTemplatedInputDirException`.
    """
    template = testdir.tmpdir.ensure('cookiecutter-fail', dir=True)

    template_config = {
        'repo_name': 'foobar',
        'short_description': 'Test Project'
    }
    template.join('cookiecutter.json').write(json.dumps(template_config))

    template.ensure('cookiecutter.repo_name', dir=True)

    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_should_fail(cookies):
            result = cookies.bake()

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None
    """)

    result = testdir.runpytest('-v', '--template={}'.format(template))

    result.stdout.fnmatch_lines([
        '*::test_bake_should_fail PASSED*',
    ])

@pytest.mark.parametrize('choice', ['mkdocs', 'sphinx', 'none'])
def test_cookies_bake_choices(testdir, choice):
    """Programmatically create a **Cookiecutter** template and make sure that
    cookies.bake() works with choice variables.
    """
    template = testdir.tmpdir.ensure('cookiecutter-choices', dir=True)
    template_config = {
        'repo_name': 'docs',
        'docs_tool': ['mkdocs', 'sphinx', 'none'],
    }
    template.join('cookiecutter.json').write(json.dumps(template_config))

    repo = template.ensure('{{cookiecutter.repo_name}}', dir=True)
    repo.join('README.rst').write("docs_tool: {{cookiecutter.docs_tool}}")

    testdir.makepyfile("""
        # -*- coding: utf-8 -*-

        def test_bake_project(cookies):
            result = cookies.bake(
                extra_context={'docs_tool': '%s'},
                template=r'%s',
            )

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'docs'
            assert result.project.isdir()

            assert result.project.join('README.rst').read() == 'docs_tool: %s'

            assert str(result) == '<Result {}>'.format(result.project)
    """ % (choice, template, choice))

    # run pytest without the template cli arg
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED*',
    ])

    result = testdir.runpytest('-v', '--template={}'.format(template))
