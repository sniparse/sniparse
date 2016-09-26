#!/usr/bin/python
# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import re
import os, sys
import json
import sqlite3
import getpass
import shutil
import pynotify
import time
from configobj import ConfigObj

from datetime import datetime, date
d = datetime.utcnow().strftime("%Y-%m-%d")

import ConfigParser

HOME = os.getenv('HOME')

cfgfile = HOME + '/.config/sniparse/prefs.cfg'

# -------------------- GET CONFIG GENERAL
if not os.path.exists(cfgfile):
    import sys
    execfile('/usr/share/sniparse/ifs/1u.py')
    sys.exit()

Config = ConfigParser.ConfigParser()
Config.read(cfgfile)

tpc = Config.get("Topic", "Name")
tpc_type = Config.get("Topic", "Type")
tpc_last = Config.get("Topic", "Last")
lgtl = Config.get("Lang", "LGTL")
lgsl = Config.get("Lang", "LGSL")
lt = Config.get("Lang", "LGT")
ls = Config.get("Lang", "LGS")
ucg = Config.getboolean("Pref", "ucg")
sds = Config.getboolean("Pref", "sds")
sws = Config.getboolean("Pref", "sws")
cmd1 = Config.get("Pref", "cmd1")
cmd2 = Config.get("Pref", "cmd2")
adds = Config.get("Addons", "keyword3")

DML = HOME + '/.sniparse/topics/' + lgtl + '/'
DCL = HOME + '/.config/sniparse/topics/' + lgtl + '/'


tpc_lst = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/.tpcs.json'
if not os.path.exists(tpc_lst):

    with open(tpc_lst, 'wb') as index:
        json.dump({'own': [], 'itll': [], 'tpcs': []}, index, indent=4)
    
with open(tpc_lst, 'rb') as index:
    indx = json.load(index)


class Topic (wx.Frame):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"New Topic", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz(wx.Size(390,125), wx.DefaultSize)
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        # ==============================================================
        self.label_name = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.label_name.Wrap( -1 )
        #self.label_name.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer4.Add( self.label_name, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 360,-1 ), 0 )
        bSizer4.Add( self.m_textCtrl1, 1, wx.ALL, 5 )
        
        
        bSizer6.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        # ==============================================================
        self.label_url1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"URL:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.label_url1.Wrap( -1 )
        self.label_url1.Hide()
        #self.label_url1.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer5.Add( self.label_url1, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.url1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer5.Add( self.url1, 1, wx.ALL, 5 )
        self.url1.Hide()
        
        self.b_url2 = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-add", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_url2.Hide()
        self.b_url2.SetBitmapDisabled( wx.NullBitmap )
        self.b_url2.SetToolTipString( u"Add other feed in topic" )
        # ==============================================================
        
        bSizer5.Add( self.b_url2, 0, wx.ALL, 5 )
        
        
        bSizer6.Add( bSizer5, 0, wx.EXPAND, 5 )
        
        bSizer52 = wx.BoxSizer( wx.HORIZONTAL )
        # ==============================================================
        self.label_url2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"URL 2:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.label_url2.Wrap( -1 )
        #self.label_url2.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.label_url2.Hide()
        
        bSizer52.Add( self.label_url2, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.url2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.url2.Hide()
        
        bSizer52.Add( self.url2, 1, wx.ALL, 5 )
        
        self.b_url3 = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-add", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        
        self.b_url3.SetBitmapDisabled( wx.NullBitmap )
        self.b_url3.Hide()
        
        bSizer52.Add( self.b_url3, 0, wx.ALL, 5 )
        # ==============================================================
        
        
        bSizer6.Add( bSizer52, 1, wx.EXPAND, 5 )
        
        bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
        # ==============================================================
        self.label_url3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"URL 3:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.label_url3.Wrap( -1 )
        #self.label_url3.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.label_url3.Hide()
        
        bSizer51.Add( self.label_url3, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.url3 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.url3.Hide()
        
        bSizer51.Add( self.url3, 1, wx.ALL, 5 )
        
        self.b_url4 = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-add", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        
        self.b_url4.SetBitmapDisabled( wx.NullBitmap )
        self.b_url4.Hide()
        
        bSizer51.Add( self.b_url4, 0, wx.ALL, 5 )
        # ==============================================================
        
        
        bSizer6.Add( bSizer51, 1, wx.EXPAND, 5 )
        
        bSizer53 = wx.BoxSizer( wx.HORIZONTAL )
        
        # ==============================================================
        self.label_url4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"URL 4:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.label_url4.Wrap( -1 )
        #self.label_url4.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.label_url4.Hide()
        
        bSizer53.Add( self.label_url4, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.url4 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.url4.Hide()
        
        bSizer53.Add( self.url4, 1, wx.ALL, 5 )
        
        self.b_url5 = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-add", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        
        self.b_url5.SetBitmapDisabled( wx.NullBitmap )
        self.b_url5.Hide()
        
        bSizer53.Add( self.b_url5, 0, wx.ALL, 5 )
        # ==============================================================
        
        bSizer6.Add( bSizer53, 1, wx.EXPAND, 5 )
        
        
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText11 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Type:", wx.DefaultPosition, wx.Size( 40,-1 ), wx.ALIGN_RIGHT )
        self.m_staticText11.Wrap( -1 )
        #self.m_staticText11.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer3.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
        
        choice_typeChoices = [ u"Normal", u"Feed" ]
        self.choice_type = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), choice_typeChoices, 0 )
        self.choice_type.SetSelection( 0 )
        bSizer3.Add( self.choice_type, 1, wx.ALIGN_BOTTOM|wx.ALL, 5 )
        
        self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Create", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button1, 0, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALL, 5 )
        
        
        bSizer6.Add( bSizer3, 0, wx.EXPAND, 5 )
        
        
        bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
        
        
        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizer1 )
        
        self.Centre( wx.BOTH )
        self.Fit()
        self.Layout()
        bSizer1.Fit( self )
        
        self.Centre( wx.BOTH )
        dw, dh = wx.DisplaySize()
        x = -1
        y = dh - 750
        self.SetPosition((x, y))
        
        self.m_button1.Bind(wx.EVT_LEFT_UP, self.DO)
        self.choice_type.Bind( wx.EVT_CHOICE, self.uiupdt )
        self.b_url2.Bind( wx.EVT_LEFT_UP, self.addurl2 )
        self.b_url3.Bind( wx.EVT_LEFT_UP, self.addurl3 )
        self.b_url4.Bind( wx.EVT_LEFT_UP, self.addurl4 )
        
        self.choice_typeChoices = choice_typeChoices
        

    # Virtual event handlers, overide them in your derived class
    def addurl2( self, event ):
        self.b_url2.Hide()
        self.url2.Show()
        self.label_url2.Show()
        self.b_url3.Show()
        self.Fit()
        self.Layout()
        
        event.Skip()
    
    def addurl3( self, event ):
        self.b_url3.Hide()
        self.url3.Show()
        self.label_url3.Show()
        self.b_url4.Show()
        self.Fit()
        self.Layout()
        
        event.Skip()
        
    def addurl4( self, event ):
        self.b_url4.Hide()
        self.url4.Show()
        self.label_url4.Show()
        self.Fit()
        self.Layout()
        
        event.Skip()

    def uiupdt(self, event):
        ch = self.choice_type.GetSelection()
        ty = (self.choice_typeChoices[ch])
        
        if ty == 'Normal':
            self.url1.Hide()
            self.label_url1.Hide()
            self.label_url2.Hide()
            self.label_url3.Hide()
            self.label_url4.Hide()
            self.url1.Hide()
            self.url2.Hide()
            self.url3.Hide()
            self.url4.Hide()
            
        else:
            self.url1.Show()
            self.label_url1.Show()
            self.b_url2.Show()
        self.Fit()
        self.Layout()
        
        event.Skip()
    
    
    def DO(self, event):
        
        self.Destroy()
        user = getpass.getuser()
        ch = self.choice_type.GetSelection()
        ty = (self.choice_typeChoices[ch])
        t = self.m_textCtrl1.GetValue()
        t = self.m_textCtrl1.GetValue()
        url = self.url1.GetValue().strip() + '\n' + self.url2.GetValue().strip() + '\n' + self.url3.GetValue().strip() + '\n' + self.url4.GetValue().strip()

        # Remove end and starting spaces (too: lstrip or rstrip)
        t = re.sub("[!|&:'@#$]", '', t)
        t = t.strip().capitalize()
        # Check on topics list if exist this name
        tpcs = indx['tpcs']
        if any(str(t) in s for s in tpcs):
            msg='Este Nombre ya esta instalado \n Se renombrara a:  ' + t + ' 1'
            title='Info'
            dlg = wx.MessageDialog(self,
                       message=msg,
                       caption=title,
                       style=wx.YES_NO | wx.ICON_INFORMATION
                      )
            ID = dlg.ShowModal()
            if ID == wx.ID_YES:
                t = t + ' 1'
            if ID == wx.ID_NO:
                print 'no'
                sys.exit()
                self.Destroy()
        # Create topic directories
        os.chdir(DML)
        os.makedirs(t)
        os.chdir(DCL)
        os.makedirs(t)
        stts = open(DML + t + '/review.cfg','w')
        if ty == 'Normal':
            print >> stts, '0.0|0|'+d
        elif ty == 'Feed':
            print >> stts, '20|20|'+d
        # Add to list topics
        own = indx['own']
        fd = indx['fd']
        itll = indx['itll']
        tpcs = indx['tpcs']
        # ------ diferent 
        if ty == 'Normal':
            own.append(t)
        elif ty == 'Feed':
            fd.append(t)
        tpcs.append(t)
        with open(tpc_lst, 'wb') as fp:
            json.dump({'own': own, 'fd': fd, 'itll': itll, 'tpcs': tpcs}, fp, indent=1)
        # Create topic database
        tpc_db = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/' + t + '/' + 'tpc'
        db = sqlite3.connect(tpc_db)
        cur = db.cursor()
        # Create topic database
        cur.execute("""CREATE TABLE Topic
                  (name TEXT, autor TEXT, 
                  category TEXT, type INTEGER, trgt TEXT, 
                  srce TEXT, note TEXT, info1 TEXT, 
                  info2 INTEGER, stts INTEGER)
               """)
        cur.execute('CREATE TABLE Items (Items TEXT)')
        cur.execute('CREATE TABLE Learning (Items TEXT)')
        cur.execute('CREATE TABLE Learned (Items TEXT)')

        cur.execute("""CREATE TABLE Sentences
                  (trgt TEXT, mrk1 TEXT, mrk2 TEXT, 
                  mrk3 TEXT, mrk4 TEXT, mrk5 TEXT, 
                  mrk6 TEXT, mrk7 TEXT, mrk INTEGER, 
                  srce TEXT, twrds TEXT, swrds TEXT, 
                  id TEXT, img TEXT, stts INTEGER, 
                  note1 TEXT, note2 TEXT, 
                  note_img TEXT, info1 TEXT)
               """)
        cur.execute("""CREATE TABLE Words
                  (trgt TEXT, grmr TEXT, srce TEXT, 
                  expl TEXT, defn TEXT, id TEXT, 
                  img TEXT, stts INTEGER, f1 INTEGER,
                   f2 INTEGER, note1 TEXT, note2 TEXT, note_img TEXT, info1 TEXT)
               """)
        cur.execute('CREATE TABLE Images (Items TEXT)')
        cur.execute('CREATE TABLE Marks (Items TEXT)')
        cur.execute('CREATE TABLE count (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx4 (Items TEXT)')
        nt = ''
        try:
            # ------ diferent 
            if ty == 'Normal':
                cur.execute("INSERT INTO Topic (name, autor, type, trgt, srce, note, stts) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (t, user, 1, lgtl, lgsl, '', 0.0))
            elif ty == 'Feed':
                cur.execute("INSERT INTO Topic (name, autor, type, trgt, srce, note, info1, stts) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (t, user, 3, lgtl, lgsl, '', url, 20))

        except sqlite3.IntegrityError:
            print('ERROR')
        db.commit()
        db.close()
        # Write topic configuration
        cfgfile = os.getenv('HOME') + '/.config/sniparse/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)
        # ojo aca tiene que cofig() leer el file primero antes de escribir
        Config.set('Topic', 'name', t)
        # ------ diferent 
        if ty == 'Normal':
            Config.set('Topic', 'type', 'own')
        elif ty == 'Feed':
            Config.set('Topic', 'type', 'feed')
        Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(os.getenv('HOME') + '/.config/sniparse/prefs.cfg','w')
        Config.write(cfgwrt)
        cfgwrt.close()
        # show notify messagge
        time.sleep(0.5)
        pynotify.init("image")
        n = pynotify.Notification(t,
          "Is your topic now",
          "/usr/share/sniparse/images/cnn.png",
       )
        n.show()
        # Menu
        menu = open(os.getenv('HOME') + '/.config/sniparse/.menu','w')
        print >>menu, t
        
        #if ty == 'Feed':
            #sys.path.insert(0, "/usr/share/sniparse")
            #execfile('/usr/share/sniparse/updt_rss.py')
        #else:
            #pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
