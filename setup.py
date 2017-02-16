#!/usr/bin/env python

from setuptools import setup
import glob

scripts = glob.glob("*.py")

setup(
    name='HiCOrient',
    version='1.1',
    description='A tool to orient ordered scaffolds in relation to each other.',
    author='Michael Alonge',
    author_email='michael.alonge@driscolls.com',
    packages=['hic_orientation'],
    package_dir={'hic_orientation': 'hic_orientation/'},
    scripts=scripts,
)
