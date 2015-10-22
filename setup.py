#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-cookies',
    version='0.1.0',
    author='Raphael Pierzina',
    author_email='raphael@hackebrot.de',
    maintainer='Raphael Pierzina',
    maintainer_email='raphael@hackebrot.de',
    license='MIT',
    url='https://github.com/hackebrot/pytest-cookies',
    description='A Pytest plugin for your Cookiecutter templates',
    long_description=read('README.rst'),
    py_modules=['pytest_cookies'],
    install_requires=[
        'pytest>=2.8.1',
        'cookiecutter>=1.2.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    entry_points={
        'pytest11': [
            'cookies = pytest_cookies',
        ],
    },
    keywords=['cookiecutter', 'pytest'],
)
