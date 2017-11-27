#!/usr/bin/python3
from gi.repository import Gio,GLib

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import signal

class light_manager:

    SCHEMA = 'org.gnome.settings-daemon.plugins.color'

    def __init__(self):
        self.gsettings = Gio.Settings.new(self.SCHEMA)

    def set_enabled(self,is_enabled):
        self.gsettings.set_boolean('night-light-enabled',is_enabled)

    def is_enabled(self):
        return self.gsettings.get_boolean('night-light-enabled')

    def get_temp(self):
        return self.gsettings.get_value('night-light-temperature').get_uint32()

    def set_temp(self,temp):
        self.gsettings.set_value('night-light-temperature',GLib.Variant.new_uint32(temp))

class night_light_indicator:

    def build_menu(self):
        menu = gtk.Menu()
        switch = gtk.CheckMenuItem("Night Light")
        switch.set_active(self.lmanager.is_enabled())
        switch.connect("activate",self.nl_toggle)
        menu.append(switch)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def quit(self,source):
        gtk.main_quit()

    def nl_toggle(self,source):
        self.lmanager.set_enabled(source.get_active())

    def __init__(self):
        self.lmanager = light_manager()
        icon_theme = gtk.IconTheme.get_default()
        indicator = appindicator.Indicator.new('indicator-nightlight',icon_theme.lookup_icon("weather-clear-night",48,0).get_filename(), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        gtk.main()

if __name__ == "__main__":
    night_light_indicator()
