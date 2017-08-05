#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pstats_print2list',
    version='1.1.7',
    description="Add to pstats library of cProfile the feature of get the result in a list with filters, limit and sort.",
    long_description=readme + '\n\n' + history,
    author="Vauxoo",
    author_email='info@vauxoo.com',
    url='https://github.com/Vauxoo/pstats-print2list',
    packages=[
        'pstats_print2list',
    ],
    package_dir={'pstats_print2list':
                 'pstats_print2list'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pstats_print2list',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
