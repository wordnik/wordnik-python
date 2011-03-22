#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='wordnik',
    version="0.5.0",
    description='Simple wrapper around the wordnik API',
    author='Robin Walsh',
    author_email='robin@wordnik.com',
    test_suite = "nose.collector",
    url='http://developer.wordnik.com',
    exclude_package_data = { '': ['test_*'] },
    packages = ['wordnik'],
    setup_requires=['nose>=0.11']
)
