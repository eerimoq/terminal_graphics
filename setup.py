#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
import re


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
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      keywords=['terminal', 'image'],
      url='https://github.com/eerimoq/terminal_graphics',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'Pillow'
      ],
      python_requires='>=3.6',
      test_suite="tests",
      entry_points = {
          'console_scripts': ['terminal_graphics=terminal_graphics:_main']
      })
