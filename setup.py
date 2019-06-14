#!/usr/bin/env python

from distutils.core import setup

setup(
    name='redelimiter'
    version='0.1dev',
    description='A simple command line utility for converting the delimiter of delimited files.',
    author='Rexy Que',
    author_email='rexy.que@gmail.com',
    url='https://www.github.com/rexyque/redelimiter',
    license='The 3-Clause BSD License',
    long_description=open('README.md').read()
    packages=['redelimiter'],
    )
