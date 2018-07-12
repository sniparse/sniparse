#!/usr/bin/python
# -*- coding: utf-8 -*- 

import wx
import wx, os
import re
import glob
from var import *
import json
import sqlite3
import time
#import pynotify
inx = indx['tpcs']
#[::-1]
dimg = 'images/'

class Topics (wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = u"Topics", pos = wx.DefaultPosition, size = wx.Size(620,580), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        #self.m_hyperlink1 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"Share     ", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_ALIGN_CENTRE )
        #self.m_hyperlink1.SetFont( wx.Font( 5, 70, 90, 90, False, wx.EmptyString ) )
        #self.m_hyperlink1.SetMaxSize( wx.Size( -1,25 ) )
        
        
        #bSizer1.Add( self.m_hyperlink1, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT, 0 )
        
        
        self.t_lst = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ALIGN_LEFT|wx.LC_ALIGN_TOP|wx.LC_ICON|wx.LC_LIST|wx.LC_NO_HEADER|wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER)

        bSizer1.Add( self.t_lst, 1, wx.ALL|wx.EXPAND, 10 )
        
        

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.add = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )

        
        bSizer31.Add( self.add, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT|wx.LEFT, 10 )
        
        
        bSizer3.Add( bSizer31, 1, wx.EXPAND, 5 )
        
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        bSizer4.Add( self.ok, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT|wx.LEFT, 10 )
        
        self.cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )

        bSizer4.Add( self.cancel, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT|wx.LEFT, 10 )
        
        
        bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer3, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre(wx.BOTH)

        self.il = wx.ImageList(42, 42)
        
        self.t_lst.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.t_lst.InsertColumn(0, '')
        self.load()
        self.t_lst.SetColumnWidth(0, 580)
        
        dw, dh = wx.DisplaySize()
        x = -1
        y = dh - 850
        self.SetPosition((x, y))
        
        self.add.Bind(wx.EVT_LEFT_UP, self.fadd)
        self.ok.Bind(wx.EVT_LEFT_UP, self.pik)
        self.cancel.Bind(wx.EVT_LEFT_UP, self.f_cancel)
        self.t_lst.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.t_lst.Bind(wx.EVT_CONTEXT_MENU, self.onContext)
        self.t_lst.Bind(wx.EVT_LEFT_DCLICK, self.DCK)
        self.icon = wx.Icon(u"/usr/share/sniparse/images/cnn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)


    def DCK(self, event):
        self.pik(event)
        event.Skip()

    def load(self):
        for t in inx:
            try:
                cnf = open(lng_dir + '/' + t + '/review.cfg').readlines()
            except:
                self.get_stts(t)
            cnf = cnf[0].strip()
            if len(cnf.split("|")) == 3:
                cnf = cnf.split("|")
                s = cnf[0].rstrip('\n')
                self.il.Add(wx.Bitmap(sdir + '/' + dimg + s))
            else:
                s = self.get_stts(t)
                self.il.Add(wx.Bitmap(sdir + '/' + dimg + str(s)))
            self.t_lst.InsertStringItem(0, t)
            self.t_lst.SetItemImage(0, inx.index(t))

    def OnSelect(self, event):
        index = event.GetIndex()
        self.tpc = inx[::-1][index]
        
    def get_stts(self, t):
        try:
            print 'i Error getting data, fix'
            from datetime import datetime, date
            d = datetime.utcnow().strftime("%Y-%m-%d")
            tdb = lng_dir + '/' + t + '/' + 'tpc'
            db = sqlite3.connect(tdb)
            cur = db.cursor()
            cur.execute("SELECT * FROM  Topic")
            flds = cur.fetchall()
            s = [i[9] for i in flds][0]
            stts = open(lng_dir + '/' + t + '/review.cfg','w')
            print >> stts, str(s%2)+'|'+str(s)+'|'+d
            return s
        except:
            pass

    def pik(self, event):
        event.Skip()
        self.Destroy()
        cfgfile = os.getenv('HOME') + '/.config/sniparse/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)
        Config.set('Topic', 'name', self.tpc)
        Config.set('Topic', 'type', 1)
        Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(os.getenv('HOME') + '/.config/sniparse/prefs.cfg','w')
        Config.write(cfgwrt)
        cfgwrt.close()
        time.sleep(0.5)
        #pynotify.init("image")
        #n = pynotify.Notification(self.tpc,
          #"Is your topic now",
          #"/usr/share/sniparse/images/logo.png",
       #)
        #n.show()
        menu = open(os.getenv('HOME') + '/.config/sniparse/.menu','w')
        print >>menu, self.tpc
        
    def fadd(self, event):
        event.Skip()
        # APRENDIDO ojo
        from tpc import create
        c = create.Topic(None)
        app = wx.App(0)
        c.Show()
        app.MainLoop()
    
    def onContext(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.details, id=self.popupID1)
            #self.popupID1.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-info", wx.ART_MENU))
            #self.Bind(wx.EVT_MENU, self.adi, id=self.popupID1)
        menu = wx.Menu()
        itemOne = menu.Append(self.popupID1, "Details")
        self.PopupMenu(menu)
        menu.Destroy()
        
    def details(self, event):
        os.system("/usr/share/sniparse/ifs/info.py &")
        event.Skip()

    def f_cancel(self, event):
        self.Close()
        event.Skip()

if __name__ == "__main__":
    app = wx.App(0)
    Topics(None).Show()
    app.MainLoop()
    

    
    
    
    
    
    
    
    
    
