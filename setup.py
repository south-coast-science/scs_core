"""
Created on 4 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
https://packaging.python.org/tutorials/packaging-projects/
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]

setuptools.setup(
    name="scs-core",
    version="1.0.1",
    author="South Coast Science",
    author_email="contact@southcoastscience.com",
    description="The root of all South Coast Science environmental monitoring applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/south-coast-science/scs_core",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
    ],
    python_requires='>3.5',
    install_requires=required,
    platforms=['any'],
)
