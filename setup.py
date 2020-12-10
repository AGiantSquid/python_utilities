#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='python_utils',
    version='1.0',
    description='Collection of useful python utilities',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
