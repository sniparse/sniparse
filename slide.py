#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os, sys
import re
from glob import glob
from var import *
import sqlite3
import time
import locale
import textwrap
from wx.lib.embeddedimage import PyEmbeddedImage
reload(sys)
sys.setdefaultencoding("utf-8")

#-----------------------------------------------------------
class Dlg(wx.Frame):
    def __init__(self, parent, id, md):
        wx.Frame.__init__(self, parent, id, '', style=wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.md = 1
        
        self.font_trgt = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
        wx.FONTWEIGHT_BOLD, False, 'Droid Sans')
        
        self.font_srce = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
        wx.FONTWEIGHT_BOLD, False, 'Droid Sans')
        
        # --------------------------------------------------------------
        self.bitmap = wx.Bitmap(u'/usr/share/sniparse/images/backg_1.png', wx.BITMAP_TYPE_PNG)
        self.iclose = wx.Bitmap(u'/usr/share/sniparse/images/close.png', wx.BITMAP_TYPE_PNG)
        self.notimage = u'/usr/share/sniparse/images/backg_2.png'
        blur = u'/usr/share/sniparse/images/blur.png'
        self.blur = wx.Bitmap(blur, wx.BITMAP_TYPE_PNG)
        # --------------------------------------------------------------
        
        w = self.bitmap.GetWidth()
        h = self.bitmap.GetHeight()
        
        self.SetClientSize((w, h))

        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetNoteShape)
        else: self.SetNoteShape()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        

        self.bitmapRegion = wx.RegionFromBitmap(self.bitmap)
        self.imageRegion = wx.RegionFromBitmap(self.iclose)

        #self.bitmapRegion.IntersectRegion(self.imageRegion)
        self.bitmapRegion.Offset(300, 0)
        
        #self.bitmapRegion.Bind( wx.EVT_MOTION, self.hover )

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)
        #self.PositionTopRight()
        self.Centre( wx.BOTH )
        self.Show(True)
        
        #-----------------------------------------------------------
        
        self.load()
        # slide show timer
        self.stime = wx.Timer(None)
        self.stime.Bind(wx.EVT_TIMER, self.play_slide)
        self.f_SlideShow()
    
    #-----------------------------------------------------------
    def load(self):
        
        self.currentItem = 0
        self.totalItems = 0
        db = sqlite3.connect(tpc_db)
        self.cur = db.cursor()
        
        self.cur.execute("select Items from marks")
        marks = self.cur.fetchall()
        self.marks_lst = [i[0] for i in marks]
        self.marks_lst = self.marks_lst[::-1]
        
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        self.learning_lst = [i[0] for i in Learning]
        self.learning_lst = self.learning_lst[::-1]
        
        if self.md == 0:
            self.items = self.learning_lst
            
        elif self.md == 1:
            self.cur.execute("select trgt from Sentences")
            Sentences = self.cur.fetchall()
            Sentences_lst = [i[0] for i in Sentences]
            if len(Sentences_lst) > 0:
                p = "(?:%s)" % "|".join(map(re.escape, Sentences_lst))
                p = re.compile(p)
                self.items = [i for i in self.learning_lst if not p.search(i)]
            else:
                self.cur.execute("select trgt from Words")
                words = self.cur.fetchall()
                self.items = [i[0] for i in words]
                print self.items

        elif self.md == 2:
            self.cur.execute("select trgt from Words")
            Words = self.cur.fetchall()
            Words_lst = [i[0] for i in Words]
            if len(Words_lst) > 0:
                p = "(?:%s)" % "|".join(map(re.escape, Words_lst))
                p = re.compile(p)
                self.items = [i for i in self.learning_lst if not p.search(i)]
            else:
                self.cur.execute("select trgt from Sentences")
                sentences = self.cur.fetchall()
                self.items = [i[0] for i in sentences]

        elif self.md == 3:
            self.items = self.marks_lst

        if len(self.items) < 0:
            sys.exit()
        else:
            self.updateItems(self.items)
        
    #-----------------------------------------------------------
    def updateItems(self, items):
        self.item = items[0]
        self.OnPaint(self.item)

    #-----------------------------------------------------------
    def f_SlideShow(self):
        self.stime.Start(8000)
        
    #-----------------------------------------------------------
    def play_slide(self, event):
        self.nextItem()

    #-----------------------------------------------------------
    def loadItem(self, Item):

        # If is a word
        if len(Item.split(' ')) == 1:
            self.loadWord(Item)

        # Is is a sentence
        elif len(Item.split(' ')) != 1:
            self.loadSentence(Item)

    #-----------------------------------------------------------
    def loadWord(self, Item):

        self.itm = Item
        
        flds = "SELECT * FROM Words WHERE trgt=?"
        try:
            self.cur.execute(flds, [(self.itm)])
        except:
            self.itm = 1
            self.cur.execute(flds, [(self.itm)])
        flds = self.cur.fetchall()
        m_id = [i[5] for i in flds][0]
        self.trgt = [i[0] for i in flds][0]
        self.srce = [i[2] for i in flds][0]
        expl = [i[3] for i in flds][0]
        self.expl = expl.replace(self.trgt.lower(), '<b>' + self.trgt.lower() + '</b>')
        self.audio = lng_dir + "/.share/audio/" + self.trgt.lower() + '.mp3'
        self.dir_tpclang = HOME + '/.sniparse/topics/' + lgtl + '/'
        image = self.dir_tpclang + ".share/images/" + self.trgt.lower() + '-0.jpg'

        self.font_trgt = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
        wx.FONTWEIGHT_BOLD, False, 'Droid Sans')
        self.font_srce = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, 
        wx.FONTWEIGHT_NORMAL, False, 'Droid Sans')
        
        dc = wx.PaintDC(self)
        dc2 = wx.PaintDC(self)
        dc.SetFont(self.font_trgt)
        dc2.SetFont(self.font_srce)
        dc.SetTextForeground('#414141')
        dc2.SetTextForeground('#414141')
        
        
        if os.path.exists(image):
            img = wx.Image(image) 
            img.Rescale(350, 310) 
            img = wx.BitmapFromImage(img) 
            self.image = img
            dc.SetTextForeground('#E1E1E1')
            dc2.SetTextForeground('#E1E1E1')
            dc.DrawBitmap(self.bitmap, 0, 0, True)
            dc.DrawBitmap(self.image, 0, 0, True)
            dc.DrawBitmap(self.blur, 0, 0, True)
            dc.DrawBitmap(self.iclose, 325, 2, True)
            dc.DrawText(self.trgt, 30, 15)
            dc2.DrawText(self.srce, 30, 45)

        else:
            self.bar = wx.Bitmap(self.notimage, wx.BITMAP_TYPE_PNG)
            dc.DrawBitmap(self.bitmap, 0, 0, True)
            dc.DrawBitmap(self.bar, 0, 0, True)
            dc.DrawBitmap(self.iclose, 325, 2, True)
            dc.DrawText(self.trgt, 30, 15)
            dc2.DrawText(self.srce, 30, 45)
        self.pronounce()

    #-----------------------------------------------------------
    def loadSentence(self, Item):

        self.itm = Item
        try:
            self.cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(self.itm)])
        except:
            self.itm = 1
            self.cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(self.itm)])
        flds = self.cur.fetchall()
        m_id = [i[12] for i in flds][0]
        self.trgt = [i[0] for i in flds][0]
        self.srce = [i[9] for i in flds][0]
        self.audio = lng_dir + "/" + self.tpc + "/" + m_id + '.mp3'
        
        self.font_trgt = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
        wx.FONTWEIGHT_BOLD, False, 'Droid Sans')
        self.font_srce = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, 
        wx.FONTWEIGHT_NORMAL, False, 'Droid Sans')
        
        dc = wx.PaintDC(self)
        dc2 = wx.PaintDC(self)
        
        dc.SetFont(self.font_trgt)
        dc2.SetFont(self.font_srce)
        dc.SetTextForeground('#414141')
        dc2.SetTextForeground('#414141')

        self.image = wx.Bitmap(self.notimage, wx.BITMAP_TYPE_PNG)
        
        trgt = textwrap.wrap(self.trgt,40)
        srce = textwrap.wrap(self.srce,60)
        
        if len(trgt) == 3:
            dca = wx.PaintDC(self)
            dcb = wx.PaintDC(self)
            dcc = wx.PaintDC(self)
            dc2a = wx.PaintDC(self)
            dc2b = wx.PaintDC(self)
            dc2c = wx.PaintDC(self)
            dca.SetFont(self.font_trgt)
            dcb.SetFont(self.font_trgt)
            dcc.SetFont(self.font_trgt)
            dc2a.SetFont(self.font_srce)
            dc2b.SetFont(self.font_srce)
            dc2c.SetFont(self.font_srce)
            dca.SetTextForeground('#414141')
            dcb.SetTextForeground('#414141')
            dcc.SetTextForeground('#414141')
            dc2a.SetTextForeground('#414141')
            dc2b.SetTextForeground('#414141')
            dc2c.SetTextForeground('#414141')
            dc.DrawBitmap(self.bitmap, 0, 0, True)
            dc.DrawBitmap(self.image, 0, 0, True)
            dc.DrawBitmap(self.iclose, 325, 2, True)
            dca.DrawText(trgt[0], 30, 15)
            try:
                dcb.DrawText(trgt[1], 30, 30)
            except:
                pass
            try:
                dcc.DrawText(trgt[2], 30, 45)
            except:
                pass
            try:
                dc2a.DrawText(srce[0], 30, 70)
            except:
                pass
            try:
                dc2b.DrawText(srce[1], 30, 85)
            except:
                pass
            try:
                dc2c.DrawText(srce[2], 30, 100)
            except:
                pass
            
        elif len(trgt) == 2:
            dca = wx.PaintDC(self)
            dcb = wx.PaintDC(self)
            dc2a = wx.PaintDC(self)
            dc2b = wx.PaintDC(self)
            dca.SetFont(self.font_trgt)
            dcb.SetFont(self.font_trgt)
            dc2a.SetFont(self.font_srce)
            dc2b.SetFont(self.font_srce)
            dca.SetTextForeground('#414141')
            dcb.SetTextForeground('#414141')
            dc2a.SetTextForeground('#414141')
            dc2b.SetTextForeground('#414141')
            dc.DrawBitmap(self.bitmap, 0, 0, True)
            dc.DrawBitmap(self.image, 0, 0, True)
            dc.DrawBitmap(self.iclose, 325, 2, True)
            dca.DrawText(trgt[0], 30, 15)
            try:
                dcb.DrawText(trgt[1], 30, 30)
            except:
                pass
            try:
                dc2a.DrawText(srce[0], 30, 55)
            except:
                pass
            try:
                dc2b.DrawText(srce[1], 30, 70)
            except:
                pass
            
        elif len(trgt) == 1:
            dc = wx.PaintDC(self)
            dc2a = wx.PaintDC(self)
            dc.SetFont(self.font_trgt)
            dc2a.SetFont(self.font_srce)
            dc.SetTextForeground('#414141')
            dc2a.SetTextForeground('#414141')
            dc.DrawBitmap(self.bitmap, 0, 0, True)
            dc.DrawBitmap(self.image, 0, 0, True)
            dc.DrawBitmap(self.iclose, 325, 2, True)
            dc.DrawText(trgt[0], 30, 15)
            try:
                dc2a.DrawText(srce[0], 30, 40)
            except:
                pass
        self.pronounce()
    
    
    def pronounce(self):
        os.environ['file'] = self.audio
        os.system('play  "$file" &')

    #-----------------------------------------------------------
    def nextItem(self):
        if self.currentItem == self.totalItems-1:
            self.currentItem = 0
        else:
            self.currentItem += 1
        self.loadItem(self.items[self.currentItem])

    #-----------------------------------------------------------
    def previousItem(self):
        if self.currentItem == 0:
            self.currentItem = self.totalItems - 1
        else:
            self.currentItem -= 1
        self.loadItem(self.items[self.currentItem])

    #-----------------------------------------------------------
    def SetNoteShape(self, *event):
        region = wx.RegionFromBitmap(self.bitmap)
        self.SetShape(region)
        
    #-----------------------------------------------------------
    def OnLeftDown(self, event):
        pos = event.GetPosition()
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZING))
        if self.bitmapRegion.ContainsPoint(pos):
            self.Close()
        x, y = self.ClientToScreen(event.GetPosition())
        ox, oy = self.GetPosition()
        dx = x - ox
        dy = y - oy
        self.delta = ((dx, dy))
        
    #-----------------------------------------------------------
    def OnLeftUp(self, event):
        self.SetCursor(wx.StockCursor(wx.CURSOR_RIGHT_ARROW))

    #-----------------------------------------------------------
    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            x, y = self.ClientToScreen(event.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
            
    #-----------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)
        self.loadItem(self.item)
    
    #-----------------------------------------------------------
    def OnClose (self, event):
        sys.exit()

if __name__ == '__main__':
    args = sys.argv
    app = wx.App()
    Dlg(None, -1, args[1])
    app.MainLoop()

