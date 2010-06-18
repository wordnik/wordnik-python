#!/usr/bin/env python

from distutils.core import setup

setup(name="wordnik",
      version="0.1",
      description="Simple wrapper around the wordnik API",
      author="Martin Marcher",
      author_email="martin@marcher.name",
      requires=['simplejson', "PyYaml", ],
      package_dir={"": "src"},
      packages=["wordnik", ],
)
