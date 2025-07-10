# vim:fenc=utf-8
#
# Copyright © 2016-2025 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import configparser
import grp
import logging
import os
import pwd

CONFIG_FILE_NAME = 'sysdweb.conf'
LOCAL_CONFIG_FILE = os.path.join('.', CONFIG_FILE_NAME)
SYSTEM_CONFIG_FILE = os.path.join('/etc', CONFIG_FILE_NAME)

logger = logging.getLogger(__name__)

def _get_config_file():
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
    logger.debug(f'XDG_CONFIG_HOME: \'{xdg_config_home}\'.')
    user_config_file = os.path.join(xdg_config_home, 'sysdweb', CONFIG_FILE_NAME)
    logger.debug(f'User config file: \'{user_config_file}\'.')
    for config_file in [LOCAL_CONFIG_FILE, user_config_file, SYSTEM_CONFIG_FILE]:
        if os.access(config_file, os.R_OK):
            logger.debug(f'Config file found: \'{config_file}\'.')
            return config_file
    raise SystemExit('No config file found.')

def configure(config, config_file=None):
    """
    Parse config and discards errors
    """
    if config_file is None:
        # Try to get one of default config locations
        config_file = _get_config_file()
    else:
        if not os.access(config_file, os.R_OK):
            raise SystemExit(f'Cannot read config file \'{config_file}\'.')
    logger.info(f'Using config file \'{config_file}\'.')

    try:
        config.read(config_file)
    except Exception as err:
        raise SystemExit(f'sysdweb config file is corrupted.\n{err}')

    # Configure valid users
    scope = config.get('DEFAULT', 'scope', fallback='system')
    if scope == 'system':
        # Get a full list of users
        users = config.get('DEFAULT', 'users', fallback=None)
        groups = config.get('DEFAULT', 'groups', fallback=None)
        users = [] if users is None else list(map(lambda u: u.strip(), users.split(',')))
        if groups is not None:
            groups = map(lambda g: g.strip(), groups.split(','))
            # Obtain usenames from groups
            for group in groups:
                try:
                    users.extend(grp.getgrnam(group)[3])
                except KeyError:
                    logger.warning(f'Group \'{group}\' not found in database, skipped.')
        # If left any user in list send to main process
        if users == []:
            logger.debug('Running in system mode, ALL system users are valid.')
        else:
            users = list(set(users)) # Remove duplicates
            users.sort() # Sort alphabetically
            logger.debug('Running in system mode, valid users \'{}\'.'.format(', '.join(users)))
            config.set('DEFAULT', 'users', ','.join(users))
    elif scope == 'user':
        # Only current user can log in
        user = pwd.getpwuid(os.getuid())[0]
        logger.info(f'Running in user mode, valid user \'{user}\'.')
        config.set('DEFAULT', 'users', user)
    else:
        raise SystemExit(f'Invalid scope \'{scope}\', must be \'system\' or \'user\'.')

    # Read all sections to check if are correctly configurated
    for section in config.sections():
        if config.get(section, 'title', fallback=None) is None:
            config.remove_section(section)
            logger.warning(f'Removed invalid section without title \'{section}\' from config.')
        else:
            unit = config.get(section, 'unit', fallback=None)
            if unit is None:
                config.remove_section(section)
                logger.warning(f'Removed invalid section without unit \'{section}\' from config.')
            else:
                if len(unit.split('.')) < 2:
                    unit = f'{unit}.service'
                    config.set(section, 'unit', unit)
                logger.debug(f'Configured section \'{section}\' for unit \'{unit}\'.')

    # If after check all sections no valid sections remain, exit with error
    if len(config.sections()) < 1:
        raise SystemExit('Error in config. No valid sections found.')

config = configparser.ConfigParser()
