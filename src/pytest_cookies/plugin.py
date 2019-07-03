# -*- coding: utf-8 -*-

import py
import pytest

from cookiecutter.main import cookiecutter
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config

USER_CONFIG = u"""
cookiecutters_dir: "{cookiecutters_dir}"
replay_dir: "{replay_dir}"
"""


class Result(object):
    """Holds the captured result of the cookiecutter project generation."""

    def __init__(self, exception=None, exit_code=0, project_dir=None, context=None):
        self.exception = exception
        self.exit_code = exit_code
        self.context = context
        self._project_dir = project_dir

    @property
    def project(self):
        if self.exception is None:
            return py.path.local(self._project_dir)
        return None

    def __repr__(self):
        if self.exception:
            return "<Result {!r}>".format(self.exception)

        return "<Result {}>".format(self.project)


class Cookies(object):
    """Class to provide convenient access to the cookiecutter API."""

    def __init__(self, template, output_factory, config_file):
        self._default_template = template
        self._output_factory = output_factory
        self._config_file = config_file
        self._counter = 0

    def _new_output_dir(self):
        dirname = "bake{:02d}".format(self._counter)
        output_dir = self._output_factory(dirname)
        self._counter += 1
        return output_dir

    def bake(self, extra_context=None, template=None):
        exception = None
        exit_code = 0
        project_dir = None
        context = None

        if template is None:
            template = self._default_template

        context_file = py.path.local(template).join("cookiecutter.json")

        try:
            # Render the context, so that we can store it on the Result
            context = prompt_for_config(
                generate_context(
                    context_file=str(context_file), extra_context=extra_context
                ),
                no_input=True,
            )

            # Run cookiecutter to generate a new project
            project_dir = cookiecutter(
                template,
                no_input=True,
                extra_context=extra_context,
                output_dir=str(self._new_output_dir()),
                config_file=str(self._config_file),
            )
        except SystemExit as e:
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:
            exception = e
            exit_code = -1

        return Result(
            exception=exception,
            exit_code=exit_code,
            project_dir=project_dir,
            context=context,
        )


@pytest.fixture(scope="session")
def _cookiecutter_config_file(tmpdir_factory):
    user_dir = tmpdir_factory.mktemp("user_dir")

    cookiecutters_dir = user_dir.mkdir("cookiecutters")
    replay_dir = user_dir.mkdir("cookiecutter_replay")

    config_text = USER_CONFIG.format(
        cookiecutters_dir=cookiecutters_dir, replay_dir=replay_dir
    )
    config_file = user_dir.join("config")

    config_file.write_text(config_text, encoding="utf8")
    return config_file


@pytest.yield_fixture
def cookies(request, tmpdir, _cookiecutter_config_file):
    """Yield an instance of the Cookies helper class that can be used to
    generate a project from a template.

    Run cookiecutter:
        result = cookies.bake(extra_context={
            'variable1': 'value1',
            'variable2': 'value2',
        })
    """
    template_dir = request.config.option.template

    output_dir = tmpdir.mkdir("cookies")
    output_factory = output_dir.mkdir

    yield Cookies(template_dir, output_factory, _cookiecutter_config_file)

    # Add option to keep generated output directories.
    if not request.config.option.keep_baked_projects:
        output_dir.remove()


def pytest_addoption(parser):
    group = parser.getgroup("cookies")
    group.addoption(
        "--template",
        action="store",
        default=".",
        dest="template",
        help="specify the template to be rendered",
        type="string",
    )

    group.addoption(
        "--keep-baked-projects",
        action="store_true",
        default=False,
        dest="keep_baked_projects",
        help="Keep projects directories generated with 'cookies.bake()'.",
    )
