# -*- coding: utf-8 -*-

import pytest

from cookiecutter.main import cookiecutter


class Cookies(object):
    """Class to provide convenient access to the cookiecutter API."""
    error = None
    project = None

    def __init__(self, template, output_dir):
        self._template = template
        self._output_dir = output_dir

    def bake(self, extra_context=None):
        try:
            project_dir = cookiecutter(
                self._template,
                no_input=True,
                extra_context=extra_context,
                output_dir=self._output_dir
            )
        except Exception as e:
            self.error = e
        else:
            self.project = project_dir


@pytest.fixture
def cookies(request, tmpdir):
    output_dir = request.config.option.output_dir

    if not output_dir:
        output_dir = str(tmpdir.mkdir('cookies_output'))

    _cookies = Cookies('.', output_dir)
    return _cookies


def pytest_addoption(parser):
    group = parser.getgroup('cookies')
    group.addoption(
        '--output-dir',
        action='store',
        dest='output_dir',
        help='Set the output directory for Cookiecutter'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')
