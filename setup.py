#!/usr/bin/env python

import setuptools

setup_params = dict(
    name='wordnik',
    version="2.0",
    description='Wordnik API for Python',
    author='Robin Walsh',
    author_email='robin@wordnik.com',
    url='http://developer.wordnik.com',
    packages = setuptools.find_packages(),
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
