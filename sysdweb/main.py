# vim:fenc=utf-8
#
# Copyright © 2016-2025 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from sysdweb.server import start

import argparse
import logging
import os

def main():
    # Get config from environment
    config = os.getenv('SYSDWEB_CONFIG')
    host   = os.getenv('SYSDWEB_HOST')
    port   = os.getenv('SYSDWEB_PORT')
    level  = os.getenv('SYSDWEB_LOGLEVEL')

    # Check loglevel environment variable
    if level:
        log_level = getattr(logging, level.upper(), None)
        if not isinstance(log_level, int):
            raise ValueError('Invalid log level: {}'.format(level))
    else:
        log_level = None

    # Set loglevel equivalents for argument parser
    log_levels = {
            1: logging.INFO,
            2: logging.DEBUG }

    # Create argument parser to get config via arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', metavar='value', default=config, help='custom configuration file path')
    parser.add_argument('-l', '--listen', metavar='value', default=host, help='listen address (host or ip), default: 127.0.0.1')
    parser.add_argument('-p', '--port', metavar='value', default=port, help='listen port, default: 10088')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='be verbose (add more v to increase verbosity)')
    args = parser.parse_args()

    # Maximum loglevel is 3 if user sends more vvv we ignore it
    args.verbose = 2 if args.verbose >= 2 else args.verbose

    # Set loglevel via argument or environment (untouched warning by default)
    if args.verbose > 0:
        log_level = log_levels[args.verbose]
    if log_level:
        logging.basicConfig(level=log_level)
        logger = logging.getLogger('sysdweb')
        logger.info('Setting loglevel to {}'.format(logging.getLevelName(log_level)))

    # Run main app
    start(args.config, args.listen, args.port)
