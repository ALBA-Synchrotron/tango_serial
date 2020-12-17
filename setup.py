#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    "connio",

]

extra_requirements = {
    "tango": ["pytango"],

}
if extra_requirements:
    extra_requirements["all"] = list(
        set.union(*(set(i) for i in extra_requirements.values())))

setup_requirements = []

test_requirements = []

setup(
    author="Alberto López Sánchez",
    author_email='ctbeamlines@cells.es',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="ALBA Python Serial with tango DeviceServer",
    entry_points={
        'console_scripts': [
            'Serial=py_ds_serial.tango.server:main [tango]',
        ],
    },
    install_requires=requirements,
    extras_require=extra_requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='py_ds_serial',
    name='py_ds_serial',
    packages=find_packages(include=['py_ds_serial', 'py_ds_serial.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/catunlock/py_ds_serial',
    version='0.1.0',
    zip_safe=False,
)
