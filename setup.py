#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sysdweb",
    version = "1.0",
    author = "Oscar Garcia Amor",
    author_email = "ogarcia@connectical.com",
    description = ("Control systemd services through Web or REST API"),
    license = "GPLv3",
    keywords = "systemd web api easy",
    url = "https://github.com/ogarcia/sysdweb",
    packages=['sysdweb'],
    long_description=read('README.md'),
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
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPLv3)",
        'Programming Language :: Python :: 3',
    ],
)
