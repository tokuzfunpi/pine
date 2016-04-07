#!/usr/bin/python
from setuptools import setup, find_packages

name = 'pine'

setup(
    name=name,
    version='0.0.1',
    description='Common Library',
    license='Apache License (2.0)',
    author='Joe.Yang',
    author_email='tokuzfunpi@gmail.com',
    url='',
    packages=find_packages(exclude=['test', 'bin']),
    package_data = {'':['*.cfg']},
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)',
    ],
    install_requires=[],
    scripts=[],
    entry_points={})
