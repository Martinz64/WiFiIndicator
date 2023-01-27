import os
import signal
import re
import threading

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import GObject

from gi.repository import GLib
from gi.repository import AppIndicator3 as appindicator

import WiFiInfo

APPINDICATOR_ID = 'WiFiIndicator'
WIFI_IFACE = 'wlp2s0'
indicator = None

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def main():
    #indicator = appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('icons/signal-excellent.svg'), appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,"network-cellular-signal-excellent-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
    
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    update_indicator(indicator)
    GLib.timeout_add(1000, update_indicator, indicator)
    gtk.main()

def update_indicator(indicator):
    iwlink = os.popen("iw %s link" % "wlp2s0").read().replace('\n',' ')
    wl = WiFiInfo.get_info_from_iwlink(iwlink)
    if wl['connected']:
        try:
            title = '%s %s %d dBm %d Mb/s (%s GHz)' % (
                wl['standard'],
                wl['ssid'],
                wl['signal'],
                wl['tx_speed'],
                ('%f' % (wl['freq']/1000)).rstrip('0')
            )

            indicator.set_label(title,"1")
            indicator.set_title(title)
            
            rssi = wl['signal']
            if rssi >= -50:
                indicator.set_icon("network-cellular-signal-excellent-symbolic")
            if rssi < -50 and rssi > -60:
                indicator.set_icon("network-cellular-signal-good-symbolic")
            if rssi < -60 and rssi > -70:
                indicator.set_icon("network-cellular-signal-ok-symbolic")
            if rssi < -70 and rssi > -87:
                indicator.set_icon("network-cellular-signal-weak-symbolic")
            if rssi < -87:
                indicator.set_icon("network-cellular-signal-none-symbolic")
        except:
            ""
    else:
        indicator.set_icon("network-cellular-signal-none-symbolic")
        indicator.set_label("","")
    
    
    return True

def build_menu():
    menu = gtk.Menu()
    menu.show_all()
    return menu

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
