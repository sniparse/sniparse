#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import wx, os
import re
import glob
from var import *
import sqlite3
#import pynotify
import time
from datetime import datetime, date
import os
import gtk
import gio
import signal
import subprocess
import appindicator
import urllib
import shutil
icon = '/usr/share/sniparse/images/tray5.png'
HOME = os.getenv('HOME')

def process(d0, d1):
    d0 = datetime.strptime(d0, "%Y-%m-%d")
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    return abs((d0 - d1).days)
d0 = datetime.utcnow().strftime("%Y-%m-%d")
inx = indx['tpcs'][::-1]
l='|'
index = 0
while index < len(inx):
    
    try:
        t = inx[index]
        fc = tpc_dir + '/review.cfg'
        #shutil.copyfile(fc, fc+'_')

        cnf = open(fc, 'r').readlines()
        cnf = cnf[0].split("|")
        s = int(cnf[1].rstrip('\n'))
        d1 = cnf[2].rstrip('\n')
        a1 = str(s%2+0.1)
        a2 = str(s%2+0.2)
        days = int(process(d0, d1))
        
        if s == 1:
            if days > 15 and days < 20:
                f = open(fc, 'w')
                print >>f, a1+l+str(s)+l+d1
                f.close()
            elif days > 20:
                f = open(fc, 'w')
                print >>f, a2+l+str(s)+l+d1
                f.close()
        elif s == 3:
            if days > 20 and days < 30:
                f = open(fc, 'w')
                print >>f, a1+l+str(s)+l+d1
                f.close()
            elif days > 30:
                f = open(fc, 'w')
                print >>f, a2+l+str(s)+l+d1
                f.close()
        elif s == 5:
            if days > 30 and days < 45:
                f = open(fc, 'w')
                print >>f, a1+l+str(s)+l+d1
                f.close()
            elif days > 45:
                f = open(fc, 'w')
                print >>f, a2+l+str(s)+l+d1
                f.close()
        elif s == 7:
            if days > 45 and days < 60:
                f = open(fc, 'w')
                print >>f, a1+l+str(s)+l+d1
                f.close()
            elif days > 60:
                f = open(fc, 'w')
                print >>f, a2+l+str(s)+l+d1
                f.close()
        elif s == 9:
            if days > 60:
                f = open(fc, 'w')
                print >>f, a1+l+str(s)+l+d1
                f.close()
    except:
        #shutil.copyfile(fc+'_', fc)
        print 'Error -> ' + t
    index += 1


class SniparseIndicator:

    cfg = os.getenv('HOME') + '/.config/sniparse/.menu'
    def __init__(self):
        self.indicator = appindicator.Indicator(icon, icon, appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.menu_items = []
        self.stts = 0
        self.change_label()
        self._on_menu_update()
        
    def _on_menu_update(self):
        self.change_label()
    
    def create_menu_label(self, label):
        item = gtk.ImageMenuItem()
        item.set_label(label)
        return item

    def create_menu_icon(self, label, icon_name):
        image = gtk.Image()
        image.set_from_icon_name(icon_name, 24)
        item = gtk.ImageMenuItem()
        item.set_label(label)
        item.set_image(image)
        item.set_always_show_image(True)
        return item

    def make_menu_items(self):
        menu_items = []
        menu_items.append(("gtk-new", self.on_Add_click))
        if self.stts == 0:
            menu_items.append(("Play", self.on_play))
        elif self.stts == 1:
            menu_items.append(("Stop", self.on_stop))
            #menu_items.append(("Next", self.on_next))
        return menu_items
        
    def change_label(self):
        menu_items = self.make_menu_items()
        try:
            m = open(self.cfg).readlines()
            menutopic = m
        except IOError:
            menutopic = []
        popup_menu = gtk.Menu()
        
        for label, callback in menu_items:
            if not label and not callback:
                item = gtk.SeparatorMenuItem()
            else:
                item = gtk.ImageMenuItem(label)
                item.connect('activate', callback)
            popup_menu.append(item)
        
        for bm in menutopic:
            label = bm.rstrip('\n')
            if not label:
                label = ""
            item = self.create_menu_icon(label, "gtk-home")
            item.connect("activate", self.on_Home)
            popup_menu.append(item)
        
        item = gtk.SeparatorMenuItem()
        popup_menu.append(item)
        item = self.create_menu_label("Topics")
        item.connect("activate", self.on_Topics_click)
        popup_menu.append(item)
        item = self.create_menu_label("Settings")
        item.connect("activate", self.on_Settings_click)
        popup_menu.append(item)
        item = gtk.SeparatorMenuItem()
        popup_menu.append(item)
        item = self.create_menu_label("Quit Sniparse")
        item.connect("activate", self.on_Quit_click)
        popup_menu.append(item)
        
        popup_menu.show_all()
        self.indicator.set_menu(popup_menu)
        self.menu_items = menu_items

    def on_Home(self, widget):
        os.system("'/usr/share/sniparse/main.py' &")

    def on_Add_click(self, widget):
        os.system("'/usr/share/sniparse/add.py' &")
        
    def on_Topics_click(self, widget):
        os.system("'/usr/share/sniparse/topics.py' &")
        
    def on_Settings_click(self, widget):
        os.system("'/usr/share/sniparse/cnfg.py' &")

    def on_play(self, widget):
        
        cfgfile = HOME + '/.config/sniparse/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)
        stts_lstmode = Config.getint("misc", "modeList")
        os.environ['mode'] = str(stts_lstmode)
        self.stts = 1
        os.system('(python /usr/share/sniparse/slide.py $mode) &')
        self._on_menu_update()
        
    def on_stop(self, widget):
        self.stts = 0
        os.system('(killall /usr/share/sniparse/slide.py) &')
        self._on_menu_update()

    def on_next(self, widget):
        os.system("killall play")

    def on_Quit_click(self, widget):
        os.system("/usr/share/sniparse/stop.sh 1")
        gtk.main_quit()
    
    def on_Topic_Changed(self, filemonitor, file, other_file, event_type):
        if event_type == gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT:
            self._on_menu_update()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())
    i = SniparseIndicator()
    file = gio.File(i.cfg)
    monitor = file.monitor_file()
    monitor.connect("changed", i.on_Topic_Changed)      
    gtk.main()
