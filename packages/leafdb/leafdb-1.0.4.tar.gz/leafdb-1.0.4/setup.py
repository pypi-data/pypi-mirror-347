#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from leafdb import __version__

setup(
  name='leafdb',
  version=__version__,
  author='Huaqing Ye',
  author_email='veginer@gmail.com',
  url='http://www.leafpy.org/',
  py_modules=['leafdb'],
  description='Leafdb library',
  long_description="Leafdb is a simple library for makeing raw SQL queries to most relational databases.",
  install_requires = ['sqlalchemy\n'],
  license="MIT license",
  platforms=["any"],
)
