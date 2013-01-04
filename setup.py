#!/usr/bin/env python

import setuptools

setup_params = dict(
    name='wordnik',
    version="2.1",
    description='Wordnik API for Python',
    author='Russell Horton',
    author_email='russ@wordnik.com',
    url='http://developer.wordnik.com',
    packages=setuptools.find_packages(),
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
