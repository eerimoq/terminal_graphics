#!/usr/bin/env python

import re

from setuptools import find_packages
from setuptools import setup


def find_version():
    return re.search(r"^__version__ = '(.*)'$",
                     open('terminal_graphics/version.py', 'r').read(),
                     re.MULTILINE).group(1)

setup(name='terminal_graphics',
      version=find_version(),
      description=('Images in the terminal.'),
      long_description=open('README.rst', 'r').read(),
      author='Erik Moqvist',
      author_email='erik.moqvist@gmail.com',
      license='MIT',
      keywords=['terminal', 'image'],
      url='https://github.com/eerimoq/terminal_graphics',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'Pillow',
          'numpy',
          'rich'
      ],
      python_requires='>=3.6',
      test_suite="tests",
      entry_points = {
          'console_scripts': ['terminal_graphics=terminal_graphics:_main']
      })
