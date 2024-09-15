import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AyatanaAppIndicator3 as appindicator
from gi.repository import Notify as notify
import json
import os
import random
import requests
import subprocess

APPINDICATOR_ID = 'myAppIndicator'

def main():
    appLogo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logo.png")
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, appLogo, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_changewallpaper = gtk.MenuItem(label='Change Wallpaper')
    item_changewallpaper.connect('activate', change_wallpaper)
    menu.append(item_changewallpaper)
    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', code_quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def code_quit(source):
    gtk.main_quit()

def change_wallpaper(source):
    urlFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data.json")
    with open(urlFile) as data_file:
        data = json.load(data_file)

    rand = random.randint(0, len(data) - 1)
    wallpaper_url = "http://" + data[rand]["Image URL"]
    wallpaper_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wallpaper.jpg")
    
    response = requests.get(wallpaper_url)
    with open(wallpaper_path, 'wb') as file:
        file.write(response.content)

    location = f"file://{wallpaper_path}"
    command = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", location]
    subprocess.run(command)
    notify.Notification.new("Earth View Wallpaper Changer", "Wallpaper changed successfully", None).show()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
