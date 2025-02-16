#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

try:
    with open(os.path.join(here, "HISTORY.rst"), encoding="utf-8") as f:
        history = f.read()
except FileNotFoundError:
    history = ""

with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open(os.path.join(here, "requirements-tests.txt"), encoding="utf-8") as f:
    test_requirements = f.read().splitlines()

setup(
    name="py-graph-EM",
    version="0.0.1",
    author="Regev Yehezkel Imra",
    author_email="regevel2006@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Graph Based EM",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="LGPL 3.0",
    keywords="Graph, EM",
    # Explicitly include the 'EM' package and its subpackages.
    packages=find_packages(include=["EM", "EM.*"]),
    include_package_data=True,
    # Remove the scripts argument and include test_em.py as a module:
    py_modules=["test_em"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Regev32/py-graph-em",
    zip_safe=False,
)
