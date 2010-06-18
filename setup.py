#!/usr/bin/env python

from distutils.core import setup

setup(name="wordnik",
      version="0.1",
      description="Simple wrapper around the wordnik API",
      author="Altay Guvench",
      author_email="aguvench@gmail.com",
      requires=['simplejson', "PyYaml", ],
      package_dir={"": "src"},
      packages=["wordnik", ],
)
