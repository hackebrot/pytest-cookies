# -*- coding: utf-8 -*-


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'cookies:',
        '*--output-dir=OUTPUT_DIR',
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
