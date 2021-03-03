# -*- coding: utf-8 -*-

import collections
import json

import pytest

pytest_plugins = "pytester"


@pytest.fixture(name="cookiecutter_template")
def fixture_cookiecutter_template(tmp_path):
    template = tmp_path

    template_config = collections.OrderedDict(
        [("repo_name", "foobar"), ("short_description", "Test Project")]
    )
    template.joinpath("cookiecutter.json").write_text(json.dumps(template_config))

    template_readme = "\n".join(
        [
            "{{cookiecutter.repo_name}}",
            "{% for _ in cookiecutter.repo_name %}={% endfor %}",
            "{{cookiecutter.short_description}}",
        ]
    )

    template.joinpath("{{cookiecutter.repo_name}}").mkdir(exist_ok=True)

    template.joinpath("README.rst").write_text(template_readme)

    return template
