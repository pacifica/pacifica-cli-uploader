#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the metadata."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-cli',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica CLI Tool',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    url='https://github.com/pacifica/pacifica-cli/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    package_data={'': ['*.json']},
    entry_points={
        'console_scripts': ['pacifica-cli=pacifica.cli.__main__:main'],
    },
    install_requires=[
        'jsonschema',
        'pacifica-downloader>=0.4.1',
        'pacifica-namespace',
        'pacifica-uploader>=0.3.1',
        'pager'
    ]
)
