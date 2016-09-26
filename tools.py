#!/usr/bin/python
# -*- coding: utf-8 -*- 

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st


def ChopText(text, size):
    textLen = len(text)
    if textLen < size:
        text = text
    else:
        text = text[0:size] + "..."
    return text


class brownser ():

    def updts(self):
        import urllib2 

        try:
            urllib2.urlopen(urllib2.Request("http://idiomind.com.ar/"))
            update = True
        except:
            update = False

        if update == True:
            msgbox = wx.MessageBox('Esta disponible una nueva version de Sniparse', 
                       'Info', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
            msgbox.Show()
            
        else:
            msgbox = wx.MessageBox('No software updates found. You are using the latest version of Sniparse', 
                       'Updates', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
            msgbox.Show()
               
    def mkdnt(self):
        webbrowser.open('http://DONATE.com')
        
    def fdbk(self):
        webbrowser.open('https://answers.launchpad.net/sniparse/+addquestion')
        
    def cmnty(self):
        webbrowser.open('https://bugs.launchpad.net/sniparse')


import wx
import webbrowser
from wx.lib.embeddedimage import PyEmbeddedImage

class Imv (wx.Dialog):
    
    def __init__(self, parent):
        

        wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(300,280), style = wx.DEFAULT_DIALOG_STYLE)
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_bitmap2 = wx.StaticBitmap(self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_bitmap2, 1, wx.ALL|wx.EXPAND, 5)
        
        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.SetDefault() 
        bSizer2.Add(self.m_button1, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        
        self.m_panel1.SetSizer(bSizer2)
        self.m_panel1.Layout()
        bSizer2.Fit(self.m_panel1)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND |wx.ALL, 5)
        
        self.SetSizer(bSizer1)
        self.Layout()
        
        self.Centre(wx.BOTH)

        self.m_button1.Bind(wx.EVT_LEFT_UP, self.cl)
        
        self.pimg()
        
        
    def pimg(self):
        
        img = wx.Image('/tmp/.img.jpg') 
        img.Rescale(280, 260)
        img = wx.BitmapFromImage(img) 
        self.m_bitmap2.SetBitmap(img)
    
    def cl(self, event):
        self.Destroy()
        event.Skip()
    

        


