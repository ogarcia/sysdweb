#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from sysdweb.server import run

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--listen', metavar='host or ip', default='0.0.0.0', help='listen address, default: 0.0.0.0')
    parser.add_argument('-p', '--port', metavar='port', default='10080', help='listen port, default: 10080')
    args = parser.parse_args()

    run(host=args.listen, port=args.port)
