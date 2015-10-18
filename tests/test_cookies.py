# -*- coding: utf-8 -*-

import json


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'cookies:',
        '*--template=TEMPLATE*',
    ])


def test_cookies_fixture(testdir):
    """Make sure that pytest accepts the `cookies` fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_valid_fixture(cookies):
            assert hasattr(cookies, 'bake')
            assert callable(cookies.bake)
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_valid_fixture PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_cookies_bake(testdir):
    """Programmatically create a **Cookiecutter** template and use `bake` to
    create a project from it.
    """
    template = testdir.tmpdir.ensure('cookiecutter-template', dir=True)

    template_config = {
        'repo_name': 'foobar',
        'short_description': 'Test Project'
    }
    template.join('cookiecutter.json').write(json.dumps(template_config))

    template_readme = '\n'.join([
        '{{cookiecutter.repo_name}}',
        '{% for _ in cookiecutter.repo_name %}={% endfor %}',
        '{{cookiecutter.short_description}}',
    ])

    repo = template.ensure('{{cookiecutter.repo_name}}', dir=True)
    repo.join('README.rst').write(template_readme)

    testdir.makepyfile("""
        def test_bake_project(cookies):
            result = cookies.bake(extra_context={'repo_name': 'helloworld'})

            assert result.exit_code == 0
            assert result.exception is None
            assert result.project.basename == 'helloworld'
            assert result.project.isdir()


        def test_bake_should_create_new_output(cookies):
            first_result = cookies.bake()
            assert first_result.project.dirname.endswith('bake00')

            second_result = cookies.bake()
            assert second_result.project.dirname.endswith('bake01')
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest('-v', '--template={}'.format(template))

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED',
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
        def test_bake_should_fail(cookies):
            result = cookies.bake()

            assert result.exit_code == -1
            assert result.exception is not None
            assert result.project is None
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest('-v', '--template={}'.format(template))

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_bake_should_fail PASSED',
    ])
