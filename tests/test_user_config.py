# -*- coding: utf-8 -*-


def test_config(pytester):
    """Make sure that pytest accepts the `cookies` fixture."""
    # create a temporary pytest test module
    pytester.makepyfile(
        """
        # -*- coding: utf-8 -*-

        import poyo


        def test_user_dir(tmpdir_factory, _cookiecutter_config_file):
            basetemp = tmpdir_factory.getbasetemp()

            assert _cookiecutter_config_file.basename == 'config'

            user_dir = _cookiecutter_config_file.dirpath()
            assert user_dir.fnmatch('user_dir?')

            assert user_dir.dirpath() == basetemp


        def test_valid_cookiecutter_config(_cookiecutter_config_file):
            config_text = _cookiecutter_config_file.read()
            config = poyo.parse_string(config_text)

            user_dir = _cookiecutter_config_file.dirpath()

            expected = {
                'cookiecutters_dir': str(user_dir.join('cookiecutters')),
                'replay_dir': str(user_dir.join('cookiecutter_replay')),
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
