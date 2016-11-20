#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from sysdweb.server import start

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', metavar='value', help='Custom configuration file path')
    parser.add_argument('-l', '--listen', metavar='value', help='listen address (host or ip), default: 127.0.0.1')
    parser.add_argument('-p', '--port', metavar='value', help='listen port, default: 10080')
    args = parser.parse_args()

    start (args.config, args.listen, args.port)
