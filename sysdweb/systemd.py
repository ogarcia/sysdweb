# vim:fenc=utf-8
#
# Copyright © 2016-2025 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from dbus import SystemBus, SessionBus, Interface, exceptions
from systemd import journal

DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'
SYSTEMD_BUSNAME = 'org.freedesktop.systemd1'
SYSTEMD_PATH = '/org/freedesktop/systemd1'
SYSTEMD_MANAGER_INTERFACE = 'org.freedesktop.systemd1.Manager'
SYSTEMD_UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'

class systemdBus(object):
    def __init__(self, user=False):
        self.bus = SessionBus() if user else SystemBus()
        systemd = self.bus.get_object(SYSTEMD_BUSNAME, SYSTEMD_PATH)
        self.manager = Interface(systemd, dbus_interface=SYSTEMD_MANAGER_INTERFACE)

    def get_unit_active_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'ActiveState')

    def get_unit_load_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'LoadState')

    def start_unit(self, unit):
        try:
            self.manager.StartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def stop_unit(self, unit):
        try:
            self.manager.StopUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def restart_unit(self, unit):
        try:
            self.manager.RestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_unit(self, unit):
        try:
            self.manager.ReloadUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_or_restart_unit(self, unit):
        try:
            self.manager.ReloadOrRestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

class Journal(object):
    def __init__(self, unit, user=False):
        self.reader = journal.Reader()
        match = f'_SYSTEMD_USER_UNIT={unit}' if user else f'_SYSTEMD_UNIT={unit}'
        self.reader.add_match(match)

    def get_tail(self, lines):
        self.reader.seek_tail()
        self.reader.get_previous(lines)
        journal_lines = ['{__REALTIME_TIMESTAMP} {MESSAGE}'.format(**value) for value in self.reader]
        self.reader.close()
        return journal_lines
