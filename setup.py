#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016-2018 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import sysdweb as project

import os
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = project.NAME,
    version = project.VERSION,
    author = project.AUTHOR_NAME,
    author_email = project.AUTHOR_EMAIL,
    description = project.DESCRIPTION,
    license = project.LICENSE,
    keywords = project.KEYWORDS,
    url = project.URL,
    long_description=read('README.md'),
    packages=find_packages(),
    install_requires=[str(x.req) for x in
                      parse_requirements('requirements.txt',
                      session=PipSession())],
    package_data={'sysdweb': [
            'templates/static/css/*',
            'templates/static/fonts/*',
            'templates/static/img/*',
            'templates/static/js/*',
            'templates/views/*'
        ]
    },
    entry_points={
        'console_scripts': [
            'sysdweb = sysdweb.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: Utilities',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/ogarcia/sysdweb/issues',
        'Source': 'https://github.com/ogarcia/sysdweb',
    },
)
