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
            assert cookies.exception is None
            assert cookies.exit_code == 0
            assert cookies.project is None
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
            cookies.bake(extra_context={'repo_name': 'helloworld'})

            assert cookies.exit_code == 0
            assert cookies.exception is None
            assert cookies.project.basename == 'helloworld'
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest('-v', '--template={}'.format(template))

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_bake_project PASSED',
    ])
