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
    version="0.6.0",
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
    description="The pytest plugin for your Cookiecutter templates. 🍪",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "cookiecutter>=1.4.0",
        "pytest>=3.3.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
    ],
    entry_points={"pytest11": ["cookies = pytest_cookies.plugin"]},
    keywords=["cookiecutter", "pytest"],
)
