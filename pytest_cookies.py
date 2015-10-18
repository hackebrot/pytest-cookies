# -*- coding: utf-8 -*-

import py
import pytest

from cookiecutter.main import cookiecutter


class Result(object):
    """Holds the captured result of the cookiecutter project generation."""

    def __init__(self, exception=None, exit_code=0, project_dir=None):
        self.exception = exception
        self.exit_code = exit_code
        self.project_dir = project_dir

    @property
    def project(self):
        if self.exception is None:
            return py.path.local(self.project_dir)
        return None

    def __repr__(self):
        return '<Result {}'.format(
            self.exception and repr(self.exception) or self.project
        )


class Cookies(object):
    """Class to provide convenient access to the cookiecutter API."""

    def __init__(self, template, output_factory):
        self._template = template
        self._output_factory = output_factory
        self._counter = 0

    def _new_output_dir(self):
        dirname = 'bake{:02d}'.format(self._counter)
        output_dir = self._output_factory(dirname)
        self._counter += 1
        return str(output_dir)

    def bake(self, extra_context=None):
        exception = None
        exit_code = 0
        project_dir = None

        try:
            project_dir = cookiecutter(
                self._template,
                no_input=True,
                extra_context=extra_context,
                output_dir=self._new_output_dir()
            )
        except SystemExit as e:
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:
            exception = e
            exit_code = -1

        return Result(exception, exit_code, project_dir)


@pytest.fixture
def cookies(request, tmpdir):
    template_dir = request.config.option.template
    output_factory = tmpdir.mkdir('cookies').mkdir

    _cookies = Cookies(template_dir, output_factory)
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
