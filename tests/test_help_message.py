# -*- coding: utf-8 -*-


def test_cookies_group(pytester):
    """Test the help message"""
    result = pytester.runpytest("--help")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["cookies:", "*--template=TEMPLATE*"])
