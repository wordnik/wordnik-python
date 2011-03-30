#!/usr/bin/env python

from setuptools import setup

setup(
    name='wordnik',
    version="1.0",
    description='Simple wrapper around the wordnik API',
    author='Robin Walsh',
    author_email='robin@wordnik.com',
    test_suite = "nose.collector",
    url='http://developer.wordnik.com',
    packages = ['wordnik' ],
    package_data={'wordnik': ['endpoints/*.json']},
    setup_requires=['nose>=0.11']
)
