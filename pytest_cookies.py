# -*- coding: utf-8 -*-

import py
import pytest

from cookiecutter.main import cookiecutter


class Cookies(object):
    """Class to provide convenient access to the cookiecutter API."""
    exception = None
    exit_code = 0
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
        except SystemExit as e:
            if e.code != 0:
                self.exception = e
            self.exit_code = e.code
        except Exception as e:
            self.exception = e
            self.exit_code = -1
        else:
            self.project = py.path.local(project_dir)


@pytest.fixture
def cookies(request, tmpdir):
    template_dir = request.config.option.template
    output_dir = str(tmpdir.mkdir('cookies'))

    _cookies = Cookies(template_dir, output_dir)
    return _cookies


def pytest_addoption(parser):
    group = parser.getgroup('cookies')
    group.addoption(
        '--template',
        action='store',
        default='.',
        dest='template',
        help='specify the template to be rendered',
        type='string',
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')
