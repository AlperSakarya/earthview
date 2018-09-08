import signal
import gi
import time
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import json
import os
from random import randint
import urllib
from gi.repository import Notify as notify


APPINDICATOR_ID = 'myappindicator'

def main():
    appLogo = os.path.dirname(os.path.realpath(__file__)) + "/logo.png"
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(appLogo), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    item_changewallpaper = gtk.MenuItem('Change Wallpaper')
    item_changewallpaper.connect('activate', changewallpaper)
    menu.append(item_changewallpaper)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', code_quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def code_quit(source):
    gtk.main_quit()


def changewallpaper(source):
    urlFile = os.path.dirname(os.path.realpath(__file__)) + "/data.json"
    with open(urlFile) as data_file:
        data = json.load(data_file)

    rand = randint(0, 1510)
    data = data[rand]
    wallpaper = data["Image URL"]
    url = "http://" + wallpaper
    wallPaper = os.path.dirname(os.path.realpath(__file__)) + "/wallpaper.jpg"
    urllib.urlretrieve(url, wallPaper)

    location = '"' + "file://" + os.path.dirname(os.path.realpath(__file__)) + "/wallpaper.jpg" + '"'
    command = "gsettings set org.gnome.desktop.background picture-uri " + location
    os.system(command)
    notify.Notification.new("<b>Earth View Wallpaper Changer</b>", "Wallpaper changed successfully", None).show()
    time.sleep(2)
    killnotification = "killall notify-osd"
    os.system(killnotification)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
