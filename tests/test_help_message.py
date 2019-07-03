# -*- coding: utf-8 -*-


def test_cookies_group(testdir):
    result = testdir.runpytest("--help")
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["cookies:", "*--template=TEMPLATE*"])
