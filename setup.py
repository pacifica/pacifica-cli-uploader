#!/usr/bin/python
"""Setup and install the metadata."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(
    name='PacificaCLIUploader',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica CLI Uploader',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    packages=['uploader_cli'],
    scripts=['CLIUploader.py'],
    entry_points={
        'console_scripts': ['CLIUploader=uploader_cli:main'],
    },
    install_requires=[str(ir.req) for ir in INSTALL_REQS]
)
