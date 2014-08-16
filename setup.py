#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of skiff.
# http://github.com/Shrugs/skiff

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Matt Condon m@cond.in


from setuptools import setup, find_packages
import os
import sys

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='skiff',
    version='0.9.2',
    description="Python library for DigitalOcean's v2 API",
    long_description='''
Python library for DigitalOcean's v2 API
''',
    keywords='digitalocean api library v2',
    author='Matt Condon',
    author_email='m@cond.in',
    url='http://github.com/Shrugs/skiff',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'requests>=2.3.0,<3.0.0'
    ],
    extras_require={
        'tests': tests_require
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'skiff=skiff.cli:main',
        ],
    },
)
