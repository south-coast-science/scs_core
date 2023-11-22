#!/usr/bin/env python3

"""
Created on 4 Sep 2020
Updated 23 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/guides/single-sourcing-package-version/

https://stackoverflow.com/questions/65841378/include-json-file-in-python-package-pypi
https://stackoverflow.com/questions/45147837/including-data-files-with-setup-py
"""

import codecs
import os
import setuptools


# --------------------------------------------------------------------------------------------------------------------

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    else:
        raise RuntimeError("Unable to find version string.")


# --------------------------------------------------------------------------------------------------------------------

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]


setuptools.setup(
    name="scs-core",
    version=get_version("src/scs_core/__init__.py"),
    author="South Coast Science",
    author_email="contact@southcoastscience.com",
    description="The root of all South Coast Science environmental monitoring applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/south-coast-science/scs_core",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    package_data={'scs_core': ['**/*.csv', '**/*.json', '**/*.me']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
    ],
    python_requires='>3.6',
    install_requires=required,
    platforms=['any'],
)
