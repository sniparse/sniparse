#!/usr/bin/python
# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import re
import os, sys
import json
import sqlite3
import getpass
from configobj import ConfigObj
import shutil
import pynotify
import time
import ConfigParser


try:
    HOME = os.getenv('HOME')
    cfgfile = HOME + '/.config/sniparse/prefs.cfg'
    Config = ConfigParser.ConfigParser()
    Config.read(cfgfile)
    tpc = Config.get("Topic", "Name")
    lgtl = Config.get("Lang", "LGTL")
    lgsl = Config.get("Lang", "LGSL")
    lt = Config.get("Lang", "LGT")
    ls = Config.get("Lang", "LGS")
    DML = HOME + '/.sniparse/topics/' + lgtl + '/'
    DCL = HOME + '/.config/sniparse/topics/' + lgtl + '/'
    DMLT = HOME + '/.sniparse/topics/' + lgtl + '/' + tpc + '/'
    DCMT = HOME + '/.config/sniparse/topics/' + lgtl + '/' + tpc + '/'
    tpc_db = HOME + '/.sniparse/topics/' + lgtl + '/' + tpc + '/' + 'tpc'
    
    tpc_lst = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/.tpcs.json'
    if not os.path.exists(tpc_lst):
        with open(tpc_lst, 'wb') as index:
            json.dump({'own': [], 'itll': [], 'tpcs': []}, index, indent=4)
    with open(tpc_lst, 'rb') as index:
        indx = json.load(index)
except:
    pass


class Topic ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'Rename', pos = wx.DefaultPosition, size = wx.Size( 390,105 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"New Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer2.Add( self.m_staticText1, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        
        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        dw, dh = wx.DisplaySize()
        x = -1
        y = dh - 780
        self.SetPosition((x, y))
        
        self.m_button1.Bind( wx.EVT_LEFT_UP, self.DO )

    # Virtual event handlers, overide them in your derived class
    def DO( self, event ):
        
        self.Destroy()
        new_name = unicode(self.m_textCtrl1.GetValue())
        user = getpass.getuser()
        
         # Remove end and starting spaces (too: lstrip or rstrip)
        new_name = re.sub("[!|&:'@#$]", '', new_name)
        new_name = new_name.strip().capitalize()
        
        # Check on topics list if exist this name
        tpcs = indx['tpcs']
        if any(str(new_name) in s for s in tpcs):
            
            msg='Este Nombre ya esta instalado \n Se renombrara a:  ' + new_name + ' 1'
            title='Info'

            dlg = wx.MessageDialog(self,
                       message=msg,
                       caption=title,
                       style=wx.YES_NO|wx.ICON_INFORMATION
                       )
                           
            ID = dlg.ShowModal()
            
            if ID == wx.ID_YES:
                new_name = new_name + ' 1'
            if ID == wx.ID_NO:
                print 'no'
                sys.exit()
                self.Destroy()
        
        ## Write topic configuration
        cfgfile = os.getenv('HOME') + '/.config/sniparse/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)

        # ojo aca tiene que cofig() leer el file primero antes de escribir
        Config.set('Topic', 'name', new_name)
        Config.set('Topic', 'type', 'own')
        Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(os.getenv('HOME') + '/.config/sniparse/prefs.cfg','w')
        Config.write(cfgwrt)
        cfgwrt.close()
        
        # Rename database value
        db = sqlite3.connect(tpc_db)
        cur = db.cursor()
        cur.execute('UPDATE Topic SET name=? WHERE name=?',
            (tpc,new_name))
        db.commit()
        
        # Rename topic directories
        os.chdir(DML)
        os.rename(tpc, new_name)
        
        # Rename in topics list
        own = indx['own']
        fd = indx['fd']
        itll = indx['itll']
        tpcs = indx['tpcs']
        
        if tpc in own:
            own.remove(tpc)
            own.insert(0,new_name)
        if tpc in itll:
            itll.remove(tpc)
            itll.insert(0,new_name)
        tpcs.remove(tpc)
        tpcs.insert(0,new_name)

        with open(tpc_lst, 'wb') as fp:
            json.dump({'own': own, 'fd': fd, 'itll': itll, 'tpcs': tpcs}, fp, indent=1)

        ## Menu
        menu = open(os.getenv('HOME') + '/.config/sniparse/.menu','w')
        print >>menu, new_name
        
        return False
