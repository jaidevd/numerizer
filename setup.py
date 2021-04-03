#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
"""
"""

from setuptools import setup, find_packages

# Setuptools config
NAME = "numerizer"
DESCRIPTION = "Python module for converting natural language numbers into ints and floats."
with open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Jaidev Deshpande'
MAINTAINER_EMAIL = 'deshpande.jaidev@gmail.com'
URL = "https://github.com/jaidevd/numerizer"
DOWNLOAD_URL = 'https://pypi.org/project/numerizer/#files'
LICENSE = 'MIT'
PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/jaidevd/numerizer/issues',
    'Documentation': 'https://github.com/jaidevd/numerizer/tree/master/README.rst',
    'Source Code': 'https://github.com/jaidevd/numerizer'
}
VERSION = '0.2.0'

# Requirements
install_requires = []

# Setup
setup(
    name=NAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=install_requires
)
