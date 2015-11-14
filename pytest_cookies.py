# -*- coding: utf-8 -*-

import json
import py
import pytest

from cookiecutter.main import cookiecutter


class Result(object):
    """Holds the captured result of the cookiecutter project generation."""

    def __init__(self, exception=None, exit_code=0, project_dir=None):
        self.exception = exception
        self.exit_code = exit_code
        self._project_dir = project_dir

    @property
    def project(self):
        if self.exception is None:
            return py.path.local(self._project_dir)
        return None

    def __repr__(self):
        return '<Result {}'.format(
            self.exception and repr(self.exception) or self.project
        )


class Cookies(object):
    """Class to provide convenient access to the cookiecutter API."""

    def __init__(self, template, output_factory, config_file):
        self._template = template
        self._output_factory = output_factory
        self._config_file = config_file
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
                output_dir=self._new_output_dir(),
                config_file=str(self._config_file)
            )
        except SystemExit as e:
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:
            exception = e
            exit_code = -1

        return Result(exception, exit_code, project_dir)


@pytest.fixture(scope='session')
def _cookiecutter_config_file(tmpdir_factory):
    user_dir = tmpdir_factory.mktemp('user_dir')

    cookiecutters_dir = user_dir.mkdir('cookiecutters')
    replay_dir = user_dir.mkdir('cookiecutter_replay')

    config_data = {
        'cookiecutters_dir': str(cookiecutters_dir),
        'replay_dir': str(replay_dir),
        'default_context': {}
    }

    config_file = user_dir.join('config')

    # Cookiecutter uses YAML which is a superset of JSON
    # JSON is included in Python's standard lib whereas YAML is not.
    config_file.write(json.dumps(config_data))
    return config_file


@pytest.fixture
def cookies(request, tmpdir, _cookiecutter_config_file):
    template_dir = request.config.option.template
    output_factory = tmpdir.mkdir('cookies').mkdir
    return Cookies(template_dir, output_factory, _cookiecutter_config_file)


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
