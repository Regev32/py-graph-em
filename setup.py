#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# Get the absolute path to this directory.
here = os.path.abspath(os.path.dirname(__file__))

# Read the contents of README.md for the long description.
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

# Try to read HISTORY.rst; if it doesn't exist, use an empty string.
try:
    with open(os.path.join(here, "HISTORY.rst"), encoding="utf-8") as f:
        history = f.read()
except FileNotFoundError:
    history = ""

# Read the requirements and test requirements files.
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
    # Explicitly include the 'EM' package and any subpackages.
    packages=find_packages(include=["EM", "EM.*"]),
    py_modules=["test_em"],
    include_package_data=True,
    # Include test_em.py as a script so it gets installed in the environment’s bin/ folder.
    scripts=["test_em.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Regev32/py-graph-em",
    zip_safe=False,
)
