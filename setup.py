#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""QTPyLib: Quantitative Trading Python Library
(https://github.com/ranaroussi/qtpylib)
Simple, event-driven algorithmic trading system written in
Python 3, that supports backtesting and live trading using
Interactive Brokers for market data and order execution.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='multitasking',
    version='0.0.4',
    description='Simple async w/o async',
    long_description=long_description,
    url='https://github.com/ranaroussi/multitasking',
    author='Ran Aroussi',
    author_email='ran@aroussi.com',
    license='LGPL',
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Development Status :: 4 - Beta',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    platforms = ['any'],
    keywords='multitasking async multitask threading',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'demo', 'demos', 'examples']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)