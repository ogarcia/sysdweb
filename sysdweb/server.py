#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from bottle import abort, response, route, run, static_file, template, TEMPLATE_PATH
from socket import gethostname
from sysdweb.config import checkConfig
from sysdweb.systemd import systemdBus

import json
import os

# Search for template path
template_paths = [ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
        '/usr/share/sysdweb/templates']
template_path = [path for path in template_paths if os.access(path, os.R_OK)]
if template_path == []:
    raise SystemExit('Templates are missing.')
TEMPLATE_PATH.insert(0, os.path.join(template_path[0], 'views'))
static_path = os.path.join(template_path[0], 'static')

# Check config
config = checkConfig()

@route('/api/v1/<service>/<action>')
def get_service_action(service, action):
    if service in config.sections():
        sdbus = systemdBus(True) if config.get('DEFAULT', 'scope', fallback='system') == 'user' else systemdBus()
        unit = config.get(service, 'unit')
        if action == 'start':
            sdbus.start_unit(unit)
            return {action: 'OK'}
        elif action == 'stop':
            sdbus.stop_unit(unit)
            return {action: 'OK'}
        elif action == 'restart':
            sdbus.restart_unit(unit)
            return {action: 'OK'}
        elif action == 'reload':
            sdbus.reload_unit(unit)
            return {action: 'OK'}
        elif action == 'reloadorrestart':
            sdbus.reload_or_restart_unit(unit)
            return {action: 'OK'}
        elif action == 'status':
            if sdbus.get_unit_load_state(unit) != 'not-found':
                return {action: str(sdbus.get_unit_active_state(unit))}
            else:
                return {action: 'not-found'}
        else:
            abort(404, 'Sorry, but cannot perform \'{}\' action.'.format(service))
    else:
        abort(404, 'Sorry, but \'{}\' is not defined in config.'.format(service))

@route('/')
def get_main():
    services = []
    for service in config.sections():
        service_status = get_service_action(service, 'status')
        if service_status['status'] == 'not-found':
            cls = 'active'
        elif service_status['status'] == 'inactive':
            cls = 'danger'
        elif service_status['status'] == 'active':
            cls = 'success'
        else:
            cls = 'warning'
        disabled_start = True if cls == 'active' or cls == 'success' else False
        disabled_stop = True if cls == 'active' or cls == 'danger' else False
        disabled_restart = True if cls == 'active' else False
        services.append({'class': cls,
            'disabled_start': disabled_start,
            'disabled_stop': disabled_stop,
            'disabled_restart': disabled_restart,
            'title': config.get(service, 'title'),
            'service': service})
    return template('index', hostname=gethostname(), services=services)

# Serve static content
@route('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root=os.path.join(static_path, 'img'))

@route('/css/<file>')
def get_css(file):
    return static_file(file, root=os.path.join(static_path, 'css'))

@route('/fonts/<file>')
def get_fonts(file):
    return static_file(file, root=os.path.join(static_path, 'fonts'))

@route('/img/<file>')
def get_img(file):
    return static_file(file, root=os.path.join(static_path, 'img'))

@route('/js/<file>')
def get_js(file):
    return static_file(file, root=os.path.join(static_path, 'js'))
