# -*- coding: utf-8 -*-

import collections
import json

import pytest

pytest_plugins = 'pytester'


@pytest.fixture(name='cookiecutter_template')
def fixture_cookiecutter_template(tmpdir):
    template = tmpdir.ensure('cookiecutter-template', dir=True)

    template_config = collections.OrderedDict([
        ('repo_name', 'foobar'),
        ('short_description', 'Test Project'),
    ])
    template.join('cookiecutter.json').write(json.dumps(template_config))

    template_readme = '\n'.join([
        '{{cookiecutter.repo_name}}',
        '{% for _ in cookiecutter.repo_name %}={% endfor %}',
        '{{cookiecutter.short_description}}',
    ])

    repo = template.ensure('{{cookiecutter.repo_name}}', dir=True)
    repo.join('README.rst').write(template_readme)

    return template
