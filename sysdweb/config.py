#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016-2018 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import configparser
import grp
import logging
import os
import pwd

def checkConfig(file=None):
    """
    Parse config and discards errors
    """
    logger = logging.getLogger('sysdweb.checkConfig')
    if file != None:
        if os.access(file, os.R_OK):
            config_file = [file]
        else:
            raise SystemExit('Cannot read config file \'{}\'.'.format(file))
    else:
        config_files = [ './sysdweb.conf',
                os.path.join(os.path.expanduser('~'), '.config/sysdweb/sysdweb.conf'),
                '/etc/sysdweb.conf' ]
        # Try to load one of config locations
        config_file = [file for file in config_files if os.access(file, os.R_OK)]
        if config_file == []:
            raise SystemExit('No config file found.')
    logger.info('Using config file \'{}\'.'.format(config_file[0]))

    config = configparser.ConfigParser()
    try:
        config.read(config_file[0])
    except Exception as e:
        err = 'sysdweb config file is corrupted.\n{0}'.format(e)
        raise SystemExit(err)

    # Configure valid users
    if config.get('DEFAULT', 'scope', fallback='system') == 'system':
        # Get a full list of users
        users = config.get('DEFAULT', 'users', fallback=None)
        groups = config.get('DEFAULT', 'groups', fallback=None)

        if users:
            users = [user.strip() for user in users.split(',')]
        else:
            users = []

        if groups:
            groups = [group.strip() for group in groups.split(',')]
            # Obtain usenames from groups
            for group in groups:
                try:
                    users.extend(grp.getgrnam(group)[3])
                except KeyError:
                    logger.warning('Group \'{}\' not found in database, skipped.'.format(group))

        # If left any user in list send to main process
        if users:
            users = list(set(users)) # Remove duplicates
            users.sort() # Sort alphabetically
            logger.debug('Running in system mode, valid users \'{}\'.'.format(', '.join(users)))
            config.set('DEFAULT', 'users', ','.join(users))
        else:
            logger.debug('Running in system mode, ALL system users are valid.')
    else:
        # Only current user can log in
        user = pwd.getpwuid(os.getuid())[0]
        logger.debug('Running in user mode, valid user \'{}\'.'.format(user))
        config.set('DEFAULT', 'users', user)

    # Read all sections to check if are correctly configurated
    for section in config.sections():
        if not config.get(section, 'title', fallback=None):
            config.remove_section(section)
            logger.warning('Removed invalid section without title \'{}\' from config.'.format(section))
        else:
            if not config.get(section, 'unit', fallback=None):
                config.remove_section(section)
                logger.warning('Removed invalid section without unit \'{}\' from config.'.format(section))
            else:
                unit = config.get(section, 'unit')
                if not '.service' in unit:
                    unit = '{}.service'.format(unit)
                    config.set(section, 'unit', unit)
                logger.debug('Configured section \'{}\' for unit \'{}\''.format(section, unit))

    # If after check all sections no valid sections remain, exit with error
    if len(config.sections()) < 1:
        raise SystemExit('Error in config. No valid sections found.')

    return config
