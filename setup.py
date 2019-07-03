#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setuptools.setup(
    name="pytest-cookies",
    version="0.4.0",
    author="Raphael Pierzina",
    author_email="raphael@hackebrot.de",
    maintainer="Raphael Pierzina",
    maintainer_email="raphael@hackebrot.de",
    license="MIT",
    url="https://github.com/hackebrot/pytest-cookies",
    project_urls={
        "Repository": "https://github.com/hackebrot/pytest-cookies",
        "Issues": "https://github.com/hackebrot/pytest-cookies/issues",
    },
    description="The pytest plugin for your Cookiecutter templates 🍪",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "arrow<0.14.0",
        "cookiecutter>=1.4.0,<=1.6.0",
        "pytest>=3.3.0,<5.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
    ],
    entry_points={"pytest11": ["cookies = pytest_cookies.plugin"]},
    keywords=["cookiecutter", "pytest"],
)
