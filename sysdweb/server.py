# vim:fenc=utf-8
#
# Copyright © 2016-2025 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from bottle import abort, auth_basic, response, route, hook, run, static_file, template, TEMPLATE_PATH
from pam import pam
from socket import gethostname
from sysdweb.config import config, configure
from sysdweb.systemd import systemdBus, Journal

import os

# Search for template path
template_paths = [ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
        '/usr/share/sysdweb/templates']
template_path = [path for path in template_paths if os.access(path, os.R_OK)]
if template_path == []:
    raise SystemExit('Templates are missing.')
TEMPLATE_PATH.insert(0, os.path.join(template_path[0], 'views'))
static_path = os.path.join(template_path[0], 'static')

# Define auth function
def login(user, password):
    users = config.get('DEFAULT', 'users', fallback=None)
    if users and not user in users.split(','):
        # User not is in the valid user list
        return False
    # Validate user with password
    return pam().authenticate(user, password)


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization'


@route('/api/<:path>', method='OPTIONS')
def api_options_handler():
    response.status = 204


@route('/api/v1/<service>/<action>')
@auth_basic(login)
def get_service_action(service, action):
    if service in config.sections():
        sdbus = systemdBus(True) if config.get('DEFAULT', 'scope', fallback='system') == 'user' else systemdBus()
        unit = config.get(service, 'unit')
        if action == 'start':
            return {action: 'OK'} if sdbus.start_unit(unit) else {action: 'Fail'}
        elif action == 'stop':
            return {action: 'OK'} if sdbus.stop_unit(unit) else {action: 'Fail'}
        elif action == 'restart':
            return {action: 'OK'} if sdbus.restart_unit(unit) else {action: 'Fail'}
        elif action == 'reload':
            return {action: 'OK'} if sdbus.reload_unit(unit) else {action: 'Fail'}
        elif action == 'reloadorrestart':
            return {action: 'OK'} if sdbus.reload_or_restart_unit(unit) else {action: 'Fail'}
        elif action == 'status':
            if sdbus.get_unit_load_state(unit) != 'not-found':
                return {action: str(sdbus.get_unit_active_state(unit))}
            else:
                return {action: 'not-found'}
        elif action == 'journal':
            return get_service_journal(service, 100)
        else:
            response.status = 400
            return {'msg': 'Sorry, but cannot perform \'{}\' action.'.format(action)}
    else:
        response.status = 400
        return {'msg': 'Sorry, but \'{}\' is not defined in config.'.format(service)}

@route('/api/v1/<service>/journal/<lines>')
@auth_basic(login)
def get_service_journal(service, lines):
    if service in config.sections():
        if get_service_action(service, 'status')['status'] == 'not-found':
            return {'journal': 'not-found'}
        try:
            lines = int(lines)
        except Exception as e:
            response.status = 500
            return {'msg': '{}'.format(e)}
        unit = config.get(service, 'unit')
        journal = Journal(unit, True) if config.get('DEFAULT', 'scope', fallback='system') == 'user' else Journal(unit)
        return {'journal': journal.get_tail(lines)}
    else:
        response.status = 400
        return {'msg': 'Sorry, but \'{}\' is not defined in config.'.format(service)}

@route('/')
@auth_basic(login)
def get_main():
    services = []
    for service in config.sections():
        service_status = get_service_action(service, 'status')
        if service_status['status'] == 'not-found':
            cls = 'light'
        elif service_status['status'] == 'inactive' or service_status['status'] == 'failed':
            cls = 'danger'
        elif service_status['status'] == 'active':
            cls = 'success'
        else:
            cls = 'warning'
        disabled_start = True if cls == 'light' or cls == 'success' else False
        disabled_stop = True if cls == 'light' or cls == 'danger' else False
        disabled_restart = True if cls == 'light' or cls == 'danger' else False
        services.append({'class': cls,
            'disabled_start': disabled_start,
            'disabled_stop': disabled_stop,
            'disabled_restart': disabled_restart,
            'title': config.get(service, 'title'),
            'service': service})
    return template('index', hostname=gethostname(), services=services)

@route('/journal/<service>')
@auth_basic(login)
def get_service_journal_page(service):
    if service in config.sections():
        if get_service_action(service, 'status')['status'] == 'not-found':
            abort(400,'Sorry, but service \'{}\' unit not found in system.'.format(config.get(service, 'title')))
        journal_lines = get_service_journal(service, 100)
        return template('journal', hostname=gethostname(), service=config.get(service, 'title'), journal=journal_lines['journal'])
    else:
        abort(400, 'Sorry, but \'{}\' is not defined in config.'.format(service))

# Serve static content
@route('/favicon.ico')
@auth_basic(login)
def get_favicon():
    return static_file('favicon.ico', root=os.path.join(static_path, 'img'))

@route('/css/<file>')
@auth_basic(login)
def get_css(file):
    return static_file(file, root=os.path.join(static_path, 'css'))

@route('/img/<file>')
@auth_basic(login)
def get_img(file):
    return static_file(file, root=os.path.join(static_path, 'img'))

@route('/js/<file>')
@auth_basic(login)
def get_js(file):
    return static_file(file, root=os.path.join(static_path, 'js'))

def start(config_file, host, port):
    # Check config
    configure(config, config_file)

    if host is None: host = config.get('DEFAULT', 'host', fallback='127.0.0.1')
    if port is None: port = config.get('DEFAULT', 'port', fallback='10088')

    # Run webserver
    run(host=host, port=port)
