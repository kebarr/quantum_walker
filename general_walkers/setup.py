#!/usr/bin/env python

import os
from setuptools import setup

for line in open(os.path.join('quantum_walk','__init__.py')):
    if '__version__ = ' in line:
        version = eval(line.split('=')[-1])
        break
else:
    raise AssertionError('__version__ = "VERSION" must be in __init.__py')

setup (
    name='quantum_walk',
    version=version,
    description='Quantum Walker',
    packages=['quantum_walk'],
    install_requires=['numpy', 'scipy'],
    include_package_data=True,
    author='Katie Barr',
    entry_points={'console_scripts': 'quantum_walk=quantum_walk.run_walk:run_walk'}
)
