# -*- coding: utf-8 -*-


def test_config(pytester):
    """Make sure that pytest accepts the `cookies` fixture."""
    # create a temporary pytest test module
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import poyo
        import re


        def test_user_dir(tmp_path_factory, _cookiecutter_config_file):
            basetemp = tmp_path_factory.getbasetemp()

            assert _cookiecutter_config_file.name == 'config'

            user_dir = _cookiecutter_config_file.parent
            assert re.match('user_dir?', user_dir.name)

            assert user_dir.parent == basetemp


        def test_valid_cookiecutter_config(_cookiecutter_config_file):
            config_text = _cookiecutter_config_file.read_text()
            config = poyo.parse_string(config_text)

            user_dir = _cookiecutter_config_file.parent

            expected = {
                'cookiecutters_dir': str(user_dir.joinpath('cookiecutters')),
                'replay_dir': str(user_dir.joinpath('cookiecutter_replay')),
            }
            assert config == expected
    """
    )

    # run pytest with the following cmd args
    result = pytester.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        ["*::test_user_dir PASSED*", "*::test_valid_cookiecutter_config PASSED*"]
    )

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
