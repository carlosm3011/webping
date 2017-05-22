#!/usr/bin/env python

from setuptools import setup 

setup(name='webping.py',
      version='0.2.1',
      description='WebPing utility',
      author='Carlos Martinez',
      author_email='carlos@lacnic.net',
      scripts=['./webping.py'],
      install_requires=['click']
     )