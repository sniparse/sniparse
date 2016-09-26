#!/usr/bin/python
# -*- coding: utf-8 -*- 

#import threading yeah
from threading import Thread
from datetime import datetime, date
import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import wx.lib.wxpTag
import wx.animate
import wx.media
import wx.aui
import wx.html
import os, sys
import re
import textwrap
import glob
import ConfigParser
import sqlite3
import time
import locale
from Xlib import display
from random import shuffle
from collections import Counter
import scrnHtml
import clipboard
from imgs import *
import json

#import wx.richtext as rt
#from glob import glob
#import wx.xrc
reload(sys)
sys.setdefaultencoding("utf-8")

HOME = os.getenv('HOME')
cfgfile = HOME + '/.config/sniparse/prefs.cfg'
Config = ConfigParser.ConfigParser()
Config.read(cfgfile)
w = Config.get("pos", "w1")
h = Config.get("pos", "h1")
x2 = Config.get("pos", "x2")
y2 = Config.get("pos", "y2")

class Topic (wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = 'Sniparse', pos = wx.DefaultPosition, size = wx.Size(int(w),int(h)), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU)
        
        self.lst_fontstyle = ['open sans', 'purisa', 'arial', 'verdana', 'serif', 'daniel', 'comic sans MS']
        self.cfgfile = cfgfile
        self.Config = Config

        self.SetSizeHintsSz(wx.Size(800,420), wx.DefaultSize)
        
        #===============================================================
        self.c_bgcolor = wx.Colour(255, 255, 255)
        self.f1_bgcolor = wx.Colour(69, 69, 69)
        self.f2_bgcolor = wx.Colour(125, 125, 125)

        #===============================================================
        self.menu = wx.MenuBar(0)
        self.m_topic = wx.Menu()
        self.menuItem1 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Mark All As Learned "+ u"\t" + u"Ctrl+a", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuItem1.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-ok", wx.ART_MENU))
        self.m_topic.AppendItem(self.menuItem1)
        
        self.menuItem2 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Mark All To Learn", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuItem2.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-refresh", wx.ART_MENU))
        self.m_topic.AppendItem(self.menuItem2)
        
        self.m_topic.AppendSeparator()

        self.m_topic.AppendSeparator()
        
        self.menuItem6 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Delete"+ u"\t" + u"Ctrl+d", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem6)
        
        self.menuItem7 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Rename"+ u"\t" + u"Ctrl+r", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem7)
        
        self.m_menuItem_info = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Details"+ u"\t" + u"Ctrl+d", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.m_menuItem_info)
        
        self.m_topic.AppendSeparator()
        
        self.menuItem_import = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Import..."+ u"\t" + u"Ctrl+i", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem_import)
        
        self.menuItem3 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Export to PDF"+ u"\t" + u"Ctrl+e", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem3)
        
        self.menuItem4 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Share"+ u"\t" + u"Ctrl+s", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem4)
        
        self.m_topic.AppendSeparator()
        
        self.menuItem5 = wx.MenuItem(self.m_topic, wx.ID_ANY, u"Exit"+ u"\t" + u"Ctrl+q", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_topic.AppendItem(self.menuItem5)
        
        self.menu.Append(self.m_topic, u"Topic") 
        
        self.m_edit = wx.Menu()
        self.menuItem19 = wx.MenuItem(self.m_edit, wx.ID_ANY, u"Edit Note"+ u"\t" + u"Ctrl+m", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_edit.AppendItem(self.menuItem19)
        
        self.menuItem9 = wx.MenuItem(self.m_edit, wx.ID_ANY, u"Preferences..."+ u"\t" + u"Ctrl+p", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_edit.AppendItem(self.menuItem9)
        
        self.menu.Append(self.m_edit, u"Edit") 
        
        self.m_view = wx.Menu()
        self.m_menuItem26 = wx.MenuItem(self.m_view, wx.ID_ANY, u"Slide Show"+ u"\t" + u"F4", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem26)
        
        self.compact_view = wx.MenuItem(self.m_view, wx.ID_ANY, u"Sildeshow in Compact Mode", wx.EmptyString, wx.ITEM_CHECK)
        self.m_view.AppendItem(self.compact_view)
        
        self.m_menuItem24 = wx.MenuItem(self.m_view, wx.ID_ANY, u"Next Note"+ u"\t" + u"F7", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem24)
        
        self.m_menuItem25 = wx.MenuItem(self.m_view, wx.ID_ANY, u"Previous Note"+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem25)
        
        self.m_view.AppendSeparator()
        
        self.m_menuItemslider = wx.MenuItem(self.m_view, 10, u"Hide Slider"+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_CHECK)
        self.m_view.AppendItem(self.m_menuItemslider)
        
        self.m_menuspanel = wx.MenuItem(self.m_view, wx.ID_ANY, u"Hide Side Panel"+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_CHECK)
        self.m_view.AppendItem(self.m_menuspanel)
        
        self.m_menufscreen = wx.MenuItem(self.m_view, 12, u"Fullscreen"+ u"\t" + u"F11", wx.EmptyString, wx.ITEM_CHECK)
        self.m_view.AppendItem(self.m_menufscreen)
        
        
        self.invert_color = wx.MenuItem(self.m_view, wx.ID_ANY, u"Invert Color", wx.EmptyString, wx.ITEM_CHECK)
        self.m_view.AppendItem(self.invert_color)
        
        self.m_view.AppendSeparator()
        
        self.m_style = wx.Menu()
        self.m_menuItem27 = wx.MenuItem(self.m_style, 0, self.lst_fontstyle[0].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem27)
        
        self.m_menuItem28 = wx.MenuItem(self.m_style, 1, self.lst_fontstyle[1].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem28)
        
        self.m_menuItem29 = wx.MenuItem(self.m_style, 2, self.lst_fontstyle[2].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem29)
        
        self.m_menuItem30 = wx.MenuItem(self.m_style, 3, self.lst_fontstyle[3].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem30)
        
        self.m_menuItem31 = wx.MenuItem(self.m_style, 4, self.lst_fontstyle[4].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem31)
        
        self.m_menuItem32 = wx.MenuItem(self.m_style, 5, self.lst_fontstyle[5].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem32)
        
        self.m_menuItem33 = wx.MenuItem(self.m_style, 6, self.lst_fontstyle[6].title(), wx.EmptyString, wx.ITEM_RADIO)
        self.m_style.AppendItem(self.m_menuItem33)
        
        self.m_view.AppendSubMenu(self.m_style, u"Typeface Topic")
        
        self.m_menuItem36 = wx.MenuItem(self.m_view, 7, u"Zoom In"+ u"\t" + u"Ctrl++", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem36)
        
        self.m_menuItem35 = wx.MenuItem(self.m_view, 8, u"Zoom Out"+ u"\t" + u"Ctrl+-", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem35)
        
        self.m_menuItem37 = wx.MenuItem(self.m_view, 9, u"Normal Size"+ u"\t" + u"Ctrl+0", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_view.AppendItem(self.m_menuItem37)
        
        self.menu.Append(self.m_view, u"View") 
        
        self.m_tools = wx.Menu()
        self.p_html_text = wx.MenuItem(self.m_tools, wx.ID_ANY, u"Process Text / Web Page"+ u"\t" + u"F5", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.p_html_text)
        
        self.m_menu21 = wx.Menu()
        self.p_audio1 = wx.MenuItem(self.m_menu21, wx.ID_ANY, u"Process Audio", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu21.AppendItem(self.p_audio1)
        
        self.p_image1 = wx.MenuItem(self.m_menu21, wx.ID_ANY, u"Process Image", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu21.AppendItem(self.p_image1)
        
        self.m_tools.AppendSubMenu(self.m_menu21, u"Addons")
        
        self.menuItem10 = wx.MenuItem(self.m_tools, wx.ID_ANY, u"Topics Saved", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_tools.AppendItem(self.menuItem10)
        
        self.m_tools.AppendSeparator()
        
        self.menu.Append(self.m_tools, u"Tools") 
        
        self.m_help = wx.Menu()
        self.m_menuItem21 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Getting Started", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.m_menuItem21)
        
        self.menuItem12 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Documentation"+ u"\t" + u"F1", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem12)
        
        self.m_menuItem41 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Tips", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.m_menuItem41)
        
        self.menuItem13 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Search Updates...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem13)
        
        self.menuItem14 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Suggestions / Ask a question...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem14)
        
        self.menuItem15 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Topics Shared", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem15)
        
        self.menuItem16 = wx.MenuItem(self.m_help, wx.ID_ANY, u"Make Donation", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem16)
        
        self.menuItem17 = wx.MenuItem(self.m_help, wx.ID_ANY, u"About...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_help.AppendItem(self.menuItem17)
        
        self.menu.Append(self.m_help, u"Help") 
        
        self.SetMenuBar(self.menu)
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        #===============================================================
        self.m_notebook1 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        
        #===============================================================
        self.tab_study = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Main = wx.BoxSizer(wx.VERTICAL)
        #self.tab_study.Disable()
        
        Top = wx.BoxSizer(wx.HORIZONTAL)
        
        self.p_bimage = wx.Panel(self.tab_study, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.p_bimage.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.p_bimage.Hide()
        
        bSizer501 = wx.BoxSizer(wx.VERTICAL)
        
        self.large_img_item = wx.StaticBitmap(self.p_bimage, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer501.Add(self.large_img_item, 1, wx.ALL|wx.EXPAND, 1)
        
        
        self.p_bimage.SetSizer(bSizer501)
        self.p_bimage.Layout()
        bSizer501.Fit(self.p_bimage)
        Top.Add(self.p_bimage, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 0)
        
        self.p_html = wx.Panel(self.tab_study, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.p_html.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        sizer_htm = wx.BoxSizer(wx.VERTICAL)
        
        self.html_field = wx.html.HtmlWindow(self.p_html, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,50), 0)
        sizer_htm.Add(self.html_field, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5)
        
    
        
        self.p_html.SetSizer(sizer_htm)
        self.p_html.Layout()
        sizer_htm.Fit(self.p_html)
        Top.Add(self.p_html, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        

        
        
        self.p_image = wx.Panel(self.tab_study, wx.ID_ANY, wx.DefaultPosition, wx.Size(280,190), wx.TAB_TRAVERSAL)
        
        bSizer50 = wx.BoxSizer(wx.VERTICAL)
        
        self.p_image2 = wx.Panel(self.p_image, wx.ID_ANY, wx.DefaultPosition, wx.Size(280,190), wx.TAB_TRAVERSAL)
        self.p_image2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        
        bSizer502 = wx.BoxSizer(wx.VERTICAL)
        
        self.img_item = wx.StaticBitmap(self.p_image2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(280,190), 0)
        bSizer502.Add(self.img_item, 0, wx.SHAPED|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        self.p_image2.SetSizer(bSizer502)
        self.p_image2.Layout()
        bSizer50.Add(self.p_image2, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.p_media = wx.Panel(self.p_image, wx.ID_ANY, wx.DefaultPosition, wx.Size(280,32), wx.TAB_TRAVERSAL)
        self.p_media.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.p_media.SetMinSize(wx.Size(-1,32))
        
        bSizer5021 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.b_play_enc = wx.BitmapButton(self.p_media, wx.ID_ANY, wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER)
        bSizer5021.Add(self.b_play_enc, 0, 0, 5)
        
        self.playbackSlider = wx.Slider(self.p_media, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        bSizer5021.Add(self.playbackSlider, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        self.playbackSlider.SetValue(0)
        
        
        self.p_media.SetSizer(bSizer5021)
        self.p_media.Layout()
        bSizer50.Add(self.p_media, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5)
        
        
        self.p_image.SetSizer(bSizer50)
        self.p_image.Layout()
        Top.Add(self.p_image, 0, wx.EXPAND, 5)
        
        
        Main.Add(Top, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        #self.stts_slider = wx.Slider(self.tab_study, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size(-1,20), wx.SL_BOTTOM|wx.SL_HORIZONTAL|wx.SL_SELRANGE|wx.SL_TOP)
        #self.stts_slider.SetBackgroundColour(wx.Colour(192, 192, 192))
        #Main.Add(self.stts_slider, 0, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5)
        #self.stts_slider.Hide()
        
        
        Botton = wx.BoxSizer(wx.HORIZONTAL)
        
        bSizer484 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_auiToolBar1 = wx.aui.AuiToolBar(self.tab_study, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,100), wx.aui.AUI_TB_HORZ_LAYOUT|wx.aui.AUI_TB_HORZ_TEXT|wx.aui.AUI_TB_NO_AUTORESIZE|wx.aui.AUI_TB_TEXT)
        self.m_auiToolBar1.SetToolSeparation(15)
        self.m_auiToolBar1.SetMargins(wx.Size(0,0))
        self.m_auiToolBar1.SetToolPacking(5)
        self.b_previous = wx.BitmapButton(self.m_auiToolBar1, wx.ID_ANY, wx.Bitmap(u"/usr/share/sniparse/images/previous.png", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER)
        self.m_auiToolBar1.AddControl(self.b_previous)
        self.b_lists = wx.BitmapButton(self.m_auiToolBar1, wx.ID_ANY, wx.Bitmap(u"/usr/share/sniparse/images/lists.png", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER)
        self.m_auiToolBar1.AddControl(self.b_lists)
        self.b_next = wx.BitmapButton(self.m_auiToolBar1, wx.ID_ANY, wx.Bitmap(u"/usr/share/sniparse/images/next.png", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER)
        self.b_next.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
        
        self.m_auiToolBar1.AddControl(self.b_next)
        self.m_auiToolBar1.Realize() 
        
        bSizer484.Add(self.m_auiToolBar1, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        Botton.Add(bSizer484, 1, wx.ALIGN_BOTTOM, 5)
        
        
        Main.Add(Botton, 0, wx.EXPAND, 5)
        
        
        self.tab_study.SetSizer(Main)
        self.tab_study.Layout()
        Main.Fit(self.tab_study)
        self.m_notebook1.AddPage(self.tab_study, u"Study", True)
        
        #===============================================================
        self.tab_practice = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        #self.tab_practice.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        Sizer_practice = wx.BoxSizer(wx.VERTICAL)
        
        Sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        
        self.panel_img = wx.Panel(self.tab_practice, wx.ID_ANY, wx.DefaultPosition, wx.Size(230,-1), wx.TAB_TRAVERSAL)
        Sizer_img = wx.BoxSizer(wx.VERTICAL)
        
        Grid_img = wx.GridSizer(0, 2, 0, 0)
        
        Sizer_img_0 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_0 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_0.SetMinSize(wx.Size(37,58)) 
        self.Panel_img_0 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Panel_img_0.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        
        SSSizer_img_0 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Q0_0 = wx.StaticBitmap(self.Panel_img_0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_0.Add(self.Q0_0, 0, 0, 5)
        
        self.Q0_1 = wx.StaticBitmap(self.Panel_img_0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_0.Add(self.Q0_1, 0, 0, 5)
        
        self.Q0_2 = wx.StaticBitmap(self.Panel_img_0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_0.Add(self.Q0_2, 0, 0, 5)
        
        self.Q0_3 = wx.StaticBitmap(self.Panel_img_0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_0.Add(self.Q0_3, 0, 0, 5)
        
        self.Q0_4 = wx.StaticBitmap(self.Panel_img_0, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_0.Add(self.Q0_4, 0, 0, 5)
        
        
        self.Panel_img_0.SetSizer(SSSizer_img_0)
        self.Panel_img_0.Layout()
        SSSizer_img_0.Fit(self.Panel_img_0)
        SSizer_img_0.Add(self.Panel_img_0, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.Panel_label_0 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Sizer2_label0 = wx.BoxSizer(wx.VERTICAL)
        
        self.labelq_0 = wx.StaticText(self.Panel_label_0, wx.ID_ANY, u"Flashcards\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.labelq_0.Wrap(-1)
        self.labelq_0.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        
        Sizer2_label0.Add(self.labelq_0, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 10)
        
        
        self.Panel_label_0.SetSizer(Sizer2_label0)
        self.Panel_label_0.Layout()
        Sizer2_label0.Fit(self.Panel_label_0)
        SSizer_img_0.Add(self.Panel_label_0, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.EXPAND, 5)
        
        
        Sizer_img_0.Add(SSizer_img_0, 0, wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        
        Grid_img.Add(Sizer_img_0, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        
        Sizer_img_1 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_1 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_1.SetMinSize(wx.Size(37,58)) 
        self.Panel_img_1 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        SSSizer_img_1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Q1_0 = wx.StaticBitmap(self.Panel_img_1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_1.Add(self.Q1_0, 0, 0, 5)
        
        self.Q1_1 = wx.StaticBitmap(self.Panel_img_1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_1.Add(self.Q1_1, 0, 0, 5)
        
        self.Q1_2 = wx.StaticBitmap(self.Panel_img_1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_1.Add(self.Q1_2, 0, 0, 5)
        
        self.Q1_3 = wx.StaticBitmap(self.Panel_img_1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_1.Add(self.Q1_3, 0, 0, 5)
        
        self.Q1_4 = wx.StaticBitmap(self.Panel_img_1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_1.Add(self.Q1_4, 0, 0, 5)
        
        
        self.Panel_img_1.SetSizer(SSSizer_img_1)
        self.Panel_img_1.Layout()
        SSSizer_img_1.Fit(self.Panel_img_1)
        SSizer_img_1.Add(self.Panel_img_1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.Panel_label_1 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Sizer2_label1 = wx.BoxSizer(wx.VERTICAL)
        
        self.labelq_1 = wx.StaticText(self.Panel_label_1, wx.ID_ANY, u"Multiple\nChoise", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.labelq_1.Wrap(-1)
        self.labelq_1.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        
        Sizer2_label1.Add(self.labelq_1, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 10)
        
        
        self.Panel_label_1.SetSizer(Sizer2_label1)
        self.Panel_label_1.Layout()
        Sizer2_label1.Fit(self.Panel_label_1)
        SSizer_img_1.Add(self.Panel_label_1, 1, wx.EXPAND|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        Sizer_img_1.Add(SSizer_img_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        
        Grid_img.Add(Sizer_img_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        
        Sizer_img_2 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_2 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_2.SetMinSize(wx.Size(37,58)) 
        self.Panel_img_2 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        SSSizer_img_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Q2_0 = wx.StaticBitmap(self.Panel_img_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_2.Add(self.Q2_0, 0, 0, 5)
        
        self.Q2_1 = wx.StaticBitmap(self.Panel_img_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_2.Add(self.Q2_1, 0, 0, 5)
        
        self.Q2_2 = wx.StaticBitmap(self.Panel_img_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_2.Add(self.Q2_2, 0, 0, 5)
        
        self.Q2_3 = wx.StaticBitmap(self.Panel_img_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_2.Add(self.Q2_3, 0, 0, 5)
        
        self.Q2_4 = wx.StaticBitmap(self.Panel_img_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_2.Add(self.Q2_4, 0, 0, 5)
        
        
        self.Panel_img_2.SetSizer(SSSizer_img_2)
        self.Panel_img_2.Layout()
        SSSizer_img_2.Fit(self.Panel_img_2)
        SSizer_img_2.Add(self.Panel_img_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.Panel_label_2 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Sizer2_label2 = wx.BoxSizer(wx.VERTICAL)
        
        self.labelq_2 = wx.StaticText(self.Panel_label_2, wx.ID_ANY, u"Recognize\nPronunciation", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.labelq_2.Wrap(-1)
        self.labelq_2.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        
        Sizer2_label2.Add(self.labelq_2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 10)
        
        
        self.Panel_label_2.SetSizer(Sizer2_label2)
        self.Panel_label_2.Layout()
        Sizer2_label2.Fit(self.Panel_label_2)
        SSizer_img_2.Add(self.Panel_label_2, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        Sizer_img_2.Add(SSizer_img_2, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        
        Grid_img.Add(Sizer_img_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 5)
        
        Sizer_img_3 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_3 = wx.BoxSizer(wx.VERTICAL)
        
        SSizer_img_3.SetMinSize(wx.Size(37,58)) 
        self.Panel_img_3 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        SSSizer_img_3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Q3_0 = wx.StaticBitmap(self.Panel_img_3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_3.Add(self.Q3_0, 0, 0, 5)
        
        self.Q3_1 = wx.StaticBitmap(self.Panel_img_3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_3.Add(self.Q3_1, 0, 0, 5)
        
        self.Q3_2 = wx.StaticBitmap(self.Panel_img_3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_3.Add(self.Q3_2, 0, 0, 5)
        
        self.Q3_3 = wx.StaticBitmap(self.Panel_img_3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_3.Add(self.Q3_3, 0, 0, 5)
        
        self.Q3_4 = wx.StaticBitmap(self.Panel_img_3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        SSSizer_img_3.Add(self.Q3_4, 0, 0, 5)
        
        
        self.Panel_img_3.SetSizer(SSSizer_img_3)
        self.Panel_img_3.Layout()
        SSSizer_img_3.Fit(self.Panel_img_3)
        SSizer_img_3.Add(self.Panel_img_3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.Panel_label_3 = wx.Panel(self.panel_img, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Sizer2_label3 = wx.BoxSizer(wx.VERTICAL)
        
        self.labelq_3 = wx.StaticText(self.Panel_label_3, wx.ID_ANY, u"Write\nSentences", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.labelq_3.Wrap(-1)
        self.labelq_3.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        
        Sizer2_label3.Add(self.labelq_3, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 10)
        
        
        self.Panel_label_3.SetSizer(Sizer2_label3)
        self.Panel_label_3.Layout()
        Sizer2_label3.Fit(self.Panel_label_3)
        SSizer_img_3.Add(self.Panel_label_3, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.LEFT, 5)
        
        
        Sizer_img_3.Add(SSizer_img_3, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        
        Grid_img.Add(Sizer_img_3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT, 5)
        
        
        Sizer_img.Add(Grid_img, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        
        self.panel_img.SetSizer(Sizer_img)
        self.panel_img.Layout()
        Sizer_horizontal.Add(self.panel_img, 0, wx.TOP|wx.EXPAND, 10)
        
        Ssizer_practice = wx.BoxSizer(wx.VERTICAL)
        
        Sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Panel_top = wx.Panel(self.tab_practice, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,18), wx.TAB_TRAVERSAL)
        self.Panel_top.SetBackgroundColour(wx.Colour(148, 148, 148))
        
        Ssizer_top = wx.BoxSizer(wx.HORIZONTAL)
        
        self.top_img = wx.StaticBitmap(self.Panel_top, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(15,10), 0)
        Ssizer_top.Add(self.top_img, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.top_info = wx.StaticText(self.Panel_top, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.top_info.Wrap(-1)
        self.top_info.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        self.top_info.SetForegroundColour(wx.Colour(255, 255, 255))
        
        Ssizer_top.Add(self.top_info, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        
        
        self.Panel_top.SetSizer(Ssizer_top)
        self.Panel_top.Layout()
        Sizer_top.Add(self.Panel_top, 1, 0, 5)
        
        
        Ssizer_practice.Add(Sizer_top, 0, wx.EXPAND, 5)
        
        self.panel_practice = wx.Panel(self.tab_practice, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_practice.SetBackgroundColour(wx.Colour(148, 148, 148))
        
        Sizer_p = wx.BoxSizer(wx.VERTICAL)
        
        Ssizer_p = wx.BoxSizer(wx.VERTICAL)
        
        self.Panel_practice_2 = wx.Panel(self.panel_practice, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Panel_practice_2.SetBackgroundColour(wx.Colour(175, 175, 175))
        
        Sssizer_p = wx.BoxSizer(wx.VERTICAL)
        
        Ssssizer_p = wx.BoxSizer(wx.VERTICAL)
        
        self.QWHtml = wx.html.HtmlWindow(self.Panel_practice_2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_NO_SELECTION|wx.html.HW_SCROLLBAR_NEVER)
        Ssssizer_p.Add(self.QWHtml, 1, wx.EXPAND|wx.BOTTOM, 5)
        
        self.Qgauge = wx.Gauge(self.Panel_practice_2, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(-1,10), wx.GA_HORIZONTAL)
        self.Qgauge.SetValue(0) 
        self.Qgauge.Hide()
        
        
        
        self.Qctext = wx.TextCtrl(self.Panel_practice_2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1,100), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_PROCESS_ENTER|wx.TE_WORDWRAP)
        self.Qctext.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        self.Qctext.Hide()
        
        Ssssizer_p.Add(self.Qctext, 0, wx.ALL|wx.EXPAND, 5)
        
        
        QlistBoxChoices = []
        self.QlistBox = wx.ListBox(self.Panel_practice_2, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,160), QlistBoxChoices, wx.LB_NEEDED_SB|wx.LB_SINGLE)
        self.QlistBox.SetFont(wx.Font(15, 70, 90, 92, False, wx.EmptyString))
        self.QlistBox.SetForegroundColour(wx.Colour(125, 125, 125))
        self.QlistBox.Hide()
        
        Ssssizer_p.Add(self.QlistBox, 0, wx.ALL|wx.EXPAND, 5)
        
        
        Ssssizer_p.Add(self.Qgauge, 0, wx.ALL|wx.EXPAND, 5)
        
        
        Sssizer_p.Add(Ssssizer_p, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        Sssssizer_p = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Q_btn_no = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Nope", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_no.SetBackgroundColour(wx.Colour(221, 166, 170))
        self.Q_btn_no.Hide()
        
        Sssssizer_p.Add(self.Q_btn_no, 1, wx.ALL|wx.EXPAND, 5)
        
        self.Q_btn_show = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Show Answer", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_show.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.Q_btn_show.Hide()
        
        Sssssizer_p.Add(self.Q_btn_show, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.Q_btn_end = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_end.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.Q_btn_end.Hide()
        
        Sssssizer_p.Add(self.Q_btn_end, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.Q_btn_next4 = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_next4.Hide()
        
        Sssssizer_p.Add(self.Q_btn_next4, 1, wx.ALL, 5)
        
        self.Q_btn_ok2 = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Next Sentence", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_ok2.Hide()
        
        Sssssizer_p.Add(self.Q_btn_ok2, 1, wx.ALL, 5)
        
        self.Q_btn_play3 = wx.BitmapButton(self.Panel_practice_2, wx.ID_ANY, wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU), wx.DefaultPosition, wx.Size(100,-1), wx.BU_AUTODRAW)
        self.Q_btn_play3.Hide()
        
        Sssssizer_p.Add(self.Q_btn_play3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.Q_btn_ok = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"I Got It", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Q_btn_ok.SetBackgroundColour(wx.Colour(204, 225, 170))
        self.Q_btn_ok.Hide()
        
        Sssssizer_p.Add(self.Q_btn_ok, 1, wx.ALL|wx.EXPAND, 5)
        
        self.Qrestartf = wx.Button(self.Panel_practice_2, wx.ID_ANY, u"Restart", wx.DefaultPosition, wx.Size(-1,40), 0)
        self.Qrestartf.Hide()
        
        Sssssizer_p.Add(self.Qrestartf, 0, wx.ALL, 5)
        
        
        Sssizer_p.Add(Sssssizer_p, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5)
        
        
        self.Panel_practice_2.SetSizer(Sssizer_p)
        self.Panel_practice_2.Layout()
        Sssizer_p.Fit(self.Panel_practice_2)
        Ssizer_p.Add(self.Panel_practice_2, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        Sizer_p.Add(Ssizer_p, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        self.panel_practice.SetSizer(Sizer_p)
        self.panel_practice.Layout()
        Sizer_p.Fit(self.panel_practice)
        Ssizer_practice.Add(self.panel_practice, 1, wx.EXPAND|wx.ALIGN_RIGHT, 2)
        
        
        Sizer_horizontal.Add(Ssizer_practice, 1, wx.EXPAND|wx.ALL, 5)
        
        
        Sizer_practice.Add(Sizer_horizontal, 1, wx.EXPAND, 20)
        
        
        self.tab_practice.SetSizer(Sizer_practice)
        self.tab_practice.Layout()
        Sizer_practice.Fit(self.tab_practice)
        self.m_notebook1.AddPage(self.tab_practice, u"Practice", False)
        
        #===============================================================
        self.tab_learning = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        Sizer_learning = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel31 = wx.Panel( self.tab_learning, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer57 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_searchCtrl1 = wx.SearchCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_searchCtrl1.ShowSearchButton( True )
        self.m_searchCtrl1.ShowCancelButton( False )
        bSizer57.Add( self.m_searchCtrl1, 1, wx.ALL, 5 )
        
        self.m_button14 = wx.Button( self.m_panel31, wx.ID_ANY, u"Mark all as learnt", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer57.Add( self.m_button14, 1, wx.RIGHT|wx.LEFT, 5 )
        
        
        self.m_panel31.SetSizer( bSizer57 )
        self.m_panel31.Layout()
        bSizer57.Fit( self.m_panel31 )
        Sizer_learning.Add( self.m_panel31, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
        
        chk_learning_lstChoices = []
        self.chk_learning_lst = wx.CheckListBox( self.tab_learning, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chk_learning_lstChoices, 0 )
        Sizer_learning.Add( self.chk_learning_lst, 1, wx.EXPAND|wx.RIGHT, 5 )
        
        
        self.tab_learning.SetSizer( Sizer_learning )
        self.tab_learning.Layout()
        Sizer_learning.Fit( self.tab_learning )
        self.m_notebook1.AddPage( self.tab_learning, u"Learning", False )
        
        #===============================================================
        self.tab_learned = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        Sizer_learned = wx.BoxSizer(wx.VERTICAL)
        
        chk_learned_lstChoices = []
        self.chk_learned_lst = wx.CheckListBox(self.tab_learned, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chk_learned_lstChoices, 0)
        Sizer_learned.Add(self.chk_learned_lst, 1, wx.EXPAND, 5)
        
        
        self.tab_learned.SetSizer(Sizer_learned)
        self.tab_learned.Layout()
        Sizer_learned.Fit(self.tab_learned)
        self.m_notebook1.AddPage(self.tab_learned, u"Learned", False)
        
        #===============================================================

        self.tab_overview = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,100 ), wx.TAB_TRAVERSAL )
        Sizer_overview = wx.BoxSizer( wx.HORIZONTAL )
        
        self.p_widgets = wx.Panel( self.tab_overview, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        Sizer_spaces = wx.BoxSizer( wx.HORIZONTAL )
        
        space_a = wx.BoxSizer( wx.VERTICAL )
        
        sb_activity = wx.StaticBoxSizer( wx.StaticBox( self.p_widgets, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )
        
        self.m_panel37 = wx.Panel( self.p_widgets, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer47 = wx.BoxSizer( wx.VERTICAL )
        
        self.label_active_topic = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Topic name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_active_topic.Wrap( -1 )
        self.label_active_topic.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
        self.label_active_topic.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.label_active_topic.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
        
        bSizer47.Add( self.label_active_topic, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
        
        bSizer53 = wx.BoxSizer( wx.VERTICAL )
        
        self.label_active_topic_info1 = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Topic name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_active_topic_info1.Wrap( -1 )
        self.label_active_topic_info1.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.label_active_topic_info1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.label_active_topic_info1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
        
        bSizer53.Add( self.label_active_topic_info1, 0, wx.ALL, 5 )
        
        self.label_active_topic_info2 = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Topic name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_active_topic_info2.Wrap( -1 )
        self.label_active_topic_info2.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.label_active_topic_info2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.label_active_topic_info2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
        
        bSizer53.Add( self.label_active_topic_info2, 0, wx.ALL, 5 )
        
        
        bSizer47.Add( bSizer53, 0, 0, 5 )
        
        self.m_button111 = wx.Button( self.m_panel37, wx.ID_ANY, u"Active", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_button111.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer47.Add( self.m_button111, 0, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_staticline1 = wx.StaticLine( self.m_panel37, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer47.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer55 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText15 = wx.StaticText( self.m_panel37, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        self.m_staticText15.Hide()
        
        bSizer55.Add( self.m_staticText15, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer571 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_button13 = wx.Button( self.m_panel37, wx.ID_ANY, u"Share", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_button13.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer571.Add( self.m_button13, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
        
        self.m_button12 = wx.Button( self.m_panel37, wx.ID_ANY, u"Files", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_button12.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer571.Add( self.m_button12, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
        
        
        bSizer55.Add( bSizer571, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
        
        
        bSizer47.Add( bSizer55, 1, wx.EXPAND|wx.TOP, 5 )
        
        
        self.m_panel37.SetSizer( bSizer47 )
        self.m_panel37.Layout()
        bSizer47.Fit( self.m_panel37 )
        sb_activity.Add( self.m_panel37, 1, wx.EXPAND, 5 )
        
        
        space_a.Add( sb_activity, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        Sizer_spaces.Add( space_a, 1, wx.EXPAND, 5 )
        
        space_c = wx.BoxSizer( wx.VERTICAL )
        
        sb_activity12 = wx.StaticBoxSizer( wx.StaticBox( self.p_widgets, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
        
        self.m_panel35 = wx.Panel( self.p_widgets, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel35.SetMinSize( wx.Size( 360,-1 ) )
        #self.m_panel35.SetMaxSize( wx.Size( 350,-1 ) )
        
        bSizer4722 = wx.BoxSizer( wx.VERTICAL )
        
        self.l_topics = wx.StaticText( self.m_panel35, wx.ID_ANY, u"Topics", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_topics.Wrap( -1 )
        self.l_topics.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.l_topics.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.l_topics.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        bSizer4722.Add( self.l_topics, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
        
        self.t_lst = wx.ListCtrl( self.m_panel35, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_AUTOARRANGE|wx.LC_HRULES|wx.LC_ICON|wx.LC_NO_HEADER|wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SMALL_ICON )
        bSizer4722.Add( self.t_lst, 1, wx.EXPAND|wx.BOTTOM, 8 )
        
        
        self.m_panel35.SetSizer( bSizer4722 )
        self.m_panel35.Layout()
        bSizer4722.Fit( self.m_panel35 )
        sb_activity12.Add( self.m_panel35, 1, 0, 5 )
        
        
        space_c.Add( sb_activity12, 1, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        Sizer_spaces.Add( space_c, 0, wx.EXPAND, 5 )
        
        
        self.p_widgets.SetSizer( Sizer_spaces )
        self.p_widgets.Layout()
        Sizer_spaces.Fit( self.p_widgets )
        Sizer_overview.Add( self.p_widgets, 1, wx.EXPAND, 5 )
        
        
        self.tab_overview.SetSizer( Sizer_overview )
        self.tab_overview.Layout()
        self.m_notebook1.AddPage( self.tab_overview, u"Overview", False )
        
        bSizer1.Add( self.m_notebook1, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
      

        # item position and list
        # ===============================
        os.system('xclip -i /dev/null')
        self.cnt_item = 0
        self.stts_changelist = False
        self.stts_firsttime = True
       

        # Timer start
        # ===============================
        self.stime = wx.Timer(None)
        self.stime.Bind(wx.EVT_TIMER, self.play_slide)
        self.watcher = wx.Timer(None)
        self.watcher.Bind(wx.EVT_TIMER, self.content_refresh)

        #self.s_changes = wx.Timer(None)
        #self.s_changes.Bind(wx.EVT_TIMER, self.preload)
        #self.s_changes.Start(1000)
        
        #Load 
        # ===============================
        #self.preload()
        self.load()
         
        
        
        
        ## ===============================
        #self.il = wx.ImageList(48, 48)
        #self.t_lst.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        #self.t_lst.InsertColumn(0, '')
        #self.t_lst.SetColumnWidth(0, 320)
        ## ===============================
        
        
        self.SetSizer(bSizer1)
        self.Layout()
        
        #self.Centre(wx.BOTH)
        self.SetPosition((int(x2), int(y2)))
        
        #Player 
        # ===============================
        self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER) # --------- !

        
        #self.Bind(wx.EVT_PAINT, self.change_cursor_in_viewer)

        # Load practice data
        self.pract_load_data()
        for x in range(4):
            self.pract_set_stats(x)

        # Load overview tab
        self.overview_load()
        


        # menu
        
        # topic
        self.Bind(wx.EVT_MENU, self.change_to_learnt, id = self.menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.change_to_learn, id = self.menuItem2.GetId())
        #self.Bind(wx.EVT_MENU_RANGE, self.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.On_close, id = self.menuItem5.GetId())
        self.Bind(wx.EVT_MENU, self.delete_topic, id = self.menuItem6.GetId())
        self.Bind(wx.EVT_MENU, self.edit_topic_import, id = self.menuItem_import.GetId())
        self.Bind(wx.EVT_MENU, self.edit_topic_rename, id = self.menuItem7.GetId())
        self.Bind(wx.EVT_MENU, self.show_panel_info, id = self.m_menuItem_info.GetId())
        # edit 
        self.Bind(wx.EVT_MENU, self.show_dialog_config, id = self.menuItem9.GetId())
        self.Bind(wx.EVT_MENU, self.edit_item, id = self.menuItem19.GetId())
        # view
        self.Bind(wx.EVT_MENU, self.on_slideshow, id = self.m_menuItem26.GetId())
        
        self.Bind(wx.EVT_MENU, self.finvert_color, id = self.invert_color.GetId())
        # ========================================================================
        self.Bind(wx.EVT_MENU, self.Next, id = self.m_menuItem24.GetId())
        self.Bind(wx.EVT_MENU, self.Previous, id = self.m_menuItem25.GetId())
        self.Bind(wx.EVT_MENU, self.Cslide, id = self.compact_view.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem27.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem28.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem29.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem30.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem31.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem32.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem33.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem35.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem36.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItem37.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuspanel.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menuItemslider.GetId())
        self.Bind(wx.EVT_MENU, self.change_font_viewer, id = self.m_menufscreen.GetId())
        
        # tools
        
        # help
        self.Bind(wx.EVT_MENU, self.show_dialog_about, id = self.menuItem17.GetId())
        self.Bind(wx.EVT_MENU, self.show_dialog_first, id = self.m_menuItem21.GetId())
        self.Bind(wx.EVT_MENU, self.show_contens, id = self.menuItem12.GetId())
        self.Bind(wx.EVT_MENU, self.tool_searchupdates, id = self.menuItem13.GetId())
        self.Bind(wx.EVT_MENU, self.tool_feedback, id = self.menuItem14.GetId())
        self.Bind(wx.EVT_MENU, self.tool_website, id = self.menuItem15.GetId())
        self.Bind(wx.EVT_MENU, self.tool_donate, id = self.menuItem16.GetId())

        #self.radioBtn1.Bind(wx.EVT_RADIOBUTTON, self.Mode)
        #self.radioBtn2.Bind(wx.EVT_RADIOBUTTON, self.Mode)
        #self.radioBtn3.Bind(wx.EVT_RADIOBUTTON, self.Mode)
        #self.radioBtn4.Bind(wx.EVT_RADIOBUTTON, self.Mode)
        
        
        #self.m_auiToolBar1.Bind(wx.EVT_TOOL, self.get_info, id = 1)
        #self.m_auiToolBar1.Bind(wx.EVT_TOOL, self.on_slideshow, id = 2)
        #self.m_auiToolBar1.Bind(wx.EVT_TOOL, self.move_item_marklist, id = 3)
        #self.m_auiToolBar1.Bind(wx.EVT_TOOL, self.edit, id = 4)
        
        self.b_previous.Bind(wx.EVT_LEFT_UP, self.Previous)
        self.b_next.Bind(wx.EVT_LEFT_UP, self.Next)
        
        #self.b_next.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        
        self.b_lists.Bind(wx.EVT_LEFT_DOWN, self.change_list)
        #self.btn.Bind(wx.EVT_LEFT_UP, self.chs_style)
        
        self.chk_learning_lst.Bind( wx.EVT_LISTBOX, self.check_action )
        self.chk_learning_lst.Bind(wx.EVT_LEFT_DCLICK, self.show_from_list)

        #self.words_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_Selected1)
        #self.html_field.Bind(wx.EVT_LEFT_UP, self.onChangeitem)
        #self.stts_slider.Bind(wx.EVT_SCROLL_LINEUP, self.Next)
        #self.stts_slider.Bind(wx.EVT_SCROLL_THUMBTRACK, self.load_this)
        #self.stts_slider.Bind(wx.EVT_SCROLL, self.load_this)
        
        self.img_item.Bind(wx.EVT_LEFT_UP, self.switch_view_img)
        self.large_img_item.Bind(wx.EVT_LEFT_UP, self.switch_view_img)

        #self.b_open.Bind(wx.EVT_TOGGLEBUTTON, self.f_open)
        #self.radioBox.Bind(wx.EVT_RADIOBOX, self.chck_grammar)
        #self.m_radioBox3.Bind(wx.EVT_RADIOBOX, self.Mode)
        
        #self.html_field.Bind(wx.EVT_CONTEXT_MENU, self.on_cellmousehover) # -------------------------------------------
        
        self.Bind(wx.EVT_CLOSE, self.On_close)

        #self.radioBox1.Bind(wx.EVT_RADIOBOX, self.conjugate)
        #self.label_img.Bind(wx.EVT_LEFT_UP, self.edit_note_image_open)
        #self.m_textCtrl4.Bind(wx.EVT_TEXT_ENTER, self.edit_note_image_close)
        #self.m_textCtrl4.Bind(wx.EVT_LEAVE_WINDOW, self.edit_note_image_close)
        #self.p_image.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.p_image.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.large_img_item.Bind(wx.EVT_MOTION, self.stts_itemlist_cur2)
        #self.large_img_item.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.Bind(wx.EVT_MOTION, self.stts_itemlist_cur1)
        
        self.html_field.Bind(wx.EVT_ENTER_WINDOW, self.change_cursor_in_viewer)
     
        self.p_html.Bind(wx.EVT_LEAVE_WINDOW, self.change_cursor_no_viewer)
        #self.html_field.Bind(wx.EVT_MOTION, self.change_cursor_in_viewer)
        #self.rtc.Bind(wx.EVT_ENTER_WINDOW, self.change_cursor_in_viewer)
        #self.rtc.Bind(wx.EVT_LEAVE_WINDOW, self.change_cursor_no_viewer)
        #self.p_html.Bind(wx.EVT_MOTION, self.change_cursor_in_viewer)
        
        self.html_field.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_iconbar_click)
        self.html_field.Bind(wx.EVT_CONTEXT_MENU, self.on_viewer_context)
        
        #self.t_lst.Bind(wx.EVT_LEFT_UP, self.change_topic)
        #self.t_lst.Bind(wx.EVT_LISTBOX, self.change_topic)
        self.t_lst.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.change_topic)

        #self.b_new_topic.Bind(wx.EVT_LEFT_UP, self.edit_topic_create)
        #self.html_field.Bind(wx.EVT_LEFT_UP, self.on_cellmousehover)
        #self.html_field.Bind(wx.EVT_COMMAND_HTML_LINK_CLICKED, self.)
        #self.html_field.Bind(wx.EVT_COMMAND_HTML_CELL_HOVER, self.on_cellmousehover)
        
        # notebooks
        self.m_notebook1.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_change_page )
        
        # tab learn -----------------------------------------------
        self.m_button14.Bind(wx.EVT_LEFT_UP, self.changes_first_list)
        
        
        
        # tab overview -----------------------------------------------
        self.m_button111.Bind(wx.EVT_LEFT_UP, self.active_topic)
        
        # practice section events
        
        self.labelq_0.Bind(wx.EVT_LEFT_UP, self.pract_type_0)
        self.labelq_0.Bind(wx.EVT_MOTION, self.pract_set_label0)
        
        self.labelq_1.Bind(wx.EVT_LEFT_UP, self.pract_type_1)
        self.labelq_1.Bind(wx.EVT_MOTION, self.pract_set_label1)
        
        self.labelq_2.Bind(wx.EVT_LEFT_UP, self.pract_type_2)
        self.labelq_2.Bind(wx.EVT_MOTION, self.pract_set_label2)
        
        self.labelq_3.Bind(wx.EVT_LEFT_UP, self.pract_type_3)
        self.labelq_3.Bind(wx.EVT_MOTION, self.pract_set_label3)
        
        self.Panel_label_0.Bind(wx.EVT_MOTION, self.pract_set_label)
        self.Panel_label_1.Bind(wx.EVT_MOTION, self.pract_set_label)
        self.Panel_label_2.Bind(wx.EVT_MOTION, self.pract_set_label)
        self.Panel_label_3.Bind(wx.EVT_MOTION, self.pract_set_label)

        #self.Panel_label_0.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.Panel_label_0.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.Panel_label_1.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.Panel_label_1.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.Panel_label_2.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.Panel_label_2.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.Panel_label_3.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.Panel_label_3.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)
        #self.QlistBox.Bind(wx.EVT_ENTER_WINDOW, self.stts_itemlist_cur2)
        #self.QlistBox.Bind(wx.EVT_LEAVE_WINDOW, self.stts_itemlist_cur1)

        self.Q_btn_no.Bind(wx.EVT_LEFT_UP, self.pract_value_no)
        self.Q_btn_ok.Bind(wx.EVT_LEFT_UP, self.pract_value_ok)
        self.Q_btn_show.Bind(wx.EVT_LEFT_UP, self.pract_change_layout)
        self.Q_btn_end.Bind(wx.EVT_LEFT_UP, self.pract_on_close)

        self.Qrestartf.Bind(wx.EVT_LEFT_UP, self.pract_restart)
        self.Q_btn_ok2.Bind(wx.EVT_LEFT_UP, self.pract_check_value)
        self.Q_btn_next4.Bind(wx.EVT_LEFT_UP, self.pract_nextitem)
        self.Q_btn_play3.Bind(wx.EVT_LEFT_UP, self.pract_pronounce)

        
        self.QlistBox.Bind(wx.EVT_LISTBOX, self.pract_type1_myvalue)
        
        #self.html_field.Bind(wx.EVT_LEFT_DOWN, self.testclip)
        
        #self.QWHtml.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_iconbar_click)
        
        # ------------------------
        self.Bind(wx.EVT_SIZE, self.change_toolBarSize)
        
        
        #self.words_list.InsertColumn(0, '', width=115)
        #self.words_list.InsertColumn(1, '', width=115)
        self.compact_view.Check(self.stts_slidemode)
        
        self.m_menuspanel.Check(self.stts_spanel)
        self.icon = wx.Icon(u"/usr/share/sniparse/images/logo.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)
        self.QWHtml.SetPage(scrnHtml.QStart(info=''))
        self.Qimg = wx.Image('/usr/share/sniparse/images/f.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.Qimg2 = wx.Image('/usr/share/sniparse/images/b.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.QWHtml.SetBackgroundColour(wx.NullColor)
        #self.bmrk =  wx.Bitmap('/usr/share/sniparse/images/bmrk.png', wx.BITMAP_TYPE_ANY)
        #self.bmrk =  wx.Bitmap('/usr/share/sniparse/images/bmrk.png', wx.BITMAP_TYPE_ANY)
        self.Qsixe_font = 26
        
        self.html_field.SetStandardFonts(size=self.stts_fontsize, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        #self.html_field.SetBorders(50) # para paractice
        
        #self.Bind(wx.EVT_KEY_DOWN, self.onKey)

        if self.stts_topic%2 != 1:
            self.update_items(self.lst_items, self.cnt_item)

        self.set_review()
        self.change_cursor_in_viewer(None)
        self.change_cursor_no_viewer(None)

        # audio podcats
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.player_timer)
        self.Bind(wx.EVT_SLIDER, self.player_seek, self.playbackSlider)
        self.b_play_enc.Bind(wx.EVT_LEFT_UP, self.player_play_stop)
        self.b_play_enc.SetLabel('Stop')
        self.p_media.SetBackgroundColour(wx.Colour(208, 208, 208))
        
        self.html_field.Bind(wx.EVT_MOUSEWHEEL, self.on_mousescroll)
        self.html_field.Bind(wx.EVT_KEY_UP, self.onKeyPress)
        
        #self.html_field.Bind(wx.EVT_LEFT_DOWN, self.on_pronounce_word)
        
        self.Bind(wx.EVT_KEY_UP, self.onKeyPress)
        
        
    def active_topic(self, event):
        self.m_button111.Enable(False)
        self.m_button12.Enable(True)
        self.m_button13.Enable(True)
        self.tpc = self.active_tpc
        self.Config.read(self.cfgfile)
        self.Config.set('Topic', 'name', self.tpc)
        self.Config.set('Topic', 'type', 1)
        self.Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(self.conf_dir + '/prefs.cfg','w')
        self.Config.write(cfgwrt)
        cfgwrt.close()
        self.load()
        self.pract_load_data()
        for x in range(4):
            self.pract_set_stats(x)
        self.panel_img.Layout()
        self.set_review()
        if self.stts_topic%2 != 1:
            self.update_items(self.lst_items, self.cnt_item)
        menu = open(self.conf_dir + '/.menu','w')
        print >>menu, self.tpc
        
        self.load_item(0)
        self.change_toolBarSize(event)
        
        
    def change_topic(self, event):
        index = event.GetIndex()
        tpc = self.lst_tpcs[::-1][index]
        if tpc != self.tpc:
            self.m_button111.Enable(True)
            self.m_button12.Enable(False)
            self.m_button13.Enable(False)
        else:
            self.m_button111.Enable(False)
            self.m_button12.Enable(True)
            self.m_button13.Enable(True)
        self.active_tpc = tpc
        self.show_topic_info()


    def on_change_page(self, event):
        self.active_tpc = self.tpc
        self.m_button111.Enable(False)
        self.m_button12.Enable(True)
        self.m_button13.Enable(True)
        self.show_topic_info()

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            self.Next(None)
        elif keycode == wx.WXK_F5:
            self.pronounce()
        elif keycode == wx.WXK_LEFT:
            self.Previous(None)
        elif keycode == wx.WXK_RIGHT:
            self.Next(None)
    

    #def preload(self, event):
        #print 'pre'
        #time.sleep(1.5)
        #self.stts_slider.Enable(False)
        #self.b_next.Enable(False)
        #self.b_previous.Enable(False)
        #self.html_field.Enable(False)
       
        ##EXPERIMENTAL
       ### ===============================================================
        #self.d = d = {}
        #self.html_field.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        #self.html_field.Bind(wx.EVT_MOTION, self.MouseMove)
        #self.html_field.Bind(wx.EVT_LEFT_UP, self.MouseUp)

    #def MouseDown(self, e):   
        #o = e.GetEventObject()
        #sx,sy = self.html_field.ScreenToClient(o.GetPositionTuple())
        #dx,dy = self.html_field.ScreenToClient(wx.GetMousePosition())
        #o._x,o._y = (sx-dx, sy-dy)
        #self.d['d'] = o

    #def MouseMove(self, e):
        #try:
            #if 'd' in self.d:
                #o = self.d['d']
                #x, y = wx.GetMousePosition()
                #o.SetPosition(wx.Point(x+o._x,y+o._y))
                #self.html_field.Refresh()
        #except: pass


    #def MouseUp(self, e):
        #try:
            #if 'd' in self.d: del self.d['d']
        #except: pass
    
    
    ### ===============================================================
        #self.haveFocus = False
        #self.logKeyUp = True
        
        #self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        
        #self.html_field.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        
        #self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        #self.html_field.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    #def OnSetFocus(self, evt):
        #self.haveFocus = True
        #self.Refresh()

    #def OnMouse(self, evt):
        #if evt.ButtonDown():
            #self.SetFocus()
            #self.tab_study.SetFocus()

    #def OnKeyUp(self, evt):
        #if self.logKeyUp:
            #self.Next(evt)
        ##if self.callSkip:
            ##evt.Skip()

    #def OnKeyUp(self, e):
        #code = e.GetKeyCode()
        #print code
        #if code == wx.WXK_RETURN:
            #print("Return")
        #e.Skip()

    #def onKey(self, event):

        #key_code = event.GetKeyCode()
        #if key_code == wx.WXK_ESCAPE:
            #self.ShowFullScreen(False)
            #self.GetParent().Close()
        #else:
            #event.Skip()
            
    #def gui(self):
        #self.m_menuItemslider.Check(self.stts_sslider)
        #if self.stts_sslider is False:
            #self.stts_slider.Hide()
        #else:
            #self.stts_slider.Hide()

    # -----------------
    def load(self):
        #try:
        HOME = os.getenv('HOME')
        self.Config.read(self.cfgfile)
        self.tpc = self.Config.get("Topic", "name")
        lgtl = self.Config.get("Lang", "lgtl")
        lgsl = self.Config.get("Lang", "lgsl")        
        
        self.conf_dir = os.path.join(HOME, '.config', 'sniparse')
        self.lng_dir = os.path.join(HOME, '.sniparse', 'topics', lgtl)
        self.lng_cdir = os.path.join(self.conf_dir, 'topics', lgtl)
        self.tpc_dir = os.path.join(self.lng_dir, self.tpc)
        self.tpc_cdir = os.path.join(self.lng_cdir, self.tpc)
        self.fl_jsn = self.lng_dir + '/.tpcs.json'
        
        self.stts_hlgrammar = self.Config.getint("misc", "pgrm")
        self.stts_slidemode = self.Config.getboolean("misc", "slide")
        self.stts_fontstyle = self.Config.getint("misc", "fontStyle")
        self.stts_fontsize = self.Config.getint("misc", "fontSize")
        self.stts_sslider = self.Config.getboolean("misc", "showslider")
        self.stts_spanel = self.Config.getboolean("misc", "showpanel")
        if self.stts_firsttime is True:
            self.stts_listmode = self.Config.getint("misc", "modeList")

        self.cnt_item = 0
        
        tpc_db = self.tpc_dir + '/tpc'
        self.db = sqlite3.connect(tpc_db)
        self.cur = self.db.cursor()
        
        self.cur.execute("PRAGMA table_info('tags')")
        tags = self.cur.fetchall()
        # get tags amount and names
        self.lst_tags = [i[1] for i in tags]
        self.cnt_tags = len(self.lst_tags)
        
        #print self.lst_tags
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        self.lst_learning = [i[0] for i in Learning]
        self.lst_learning = self.lst_learning[::-1]
        self.cur.execute("select Items from Learned")
        Learned = self.cur.fetchall()
        self.lst_learned = [i[0] for i in Learned]
        self.lst_learned = self.lst_learned[::-1]
        self.cur.execute("select Items from marks")
        marks = self.cur.fetchall()
        marks = [i[0] for i in marks]
        self.lst_marks = marks[::-1]
        self.cur.execute("SELECT * FROM  Topic")
        self.flds = self.cur.fetchall()
        self.stts_topic = [i[9] for i in self.flds][0]
        self.tpy = [i[3] for i in self.flds][0]
        self.note = [i[6] for i in self.flds][0]
        print(self.tpy)

        #self.stts_fontstyle = [i[10] for i in self.flds][0]
        #self.stts_fontsize = [i[11] for i in self.flds][0]
        #self.stts_listmode = [i[12] for i in self.flds][0]
        #self.cnt_item = [i[13] for i in self.flds][0]
        
        self.Q_number = int
        self.stts_viewimg = False
        self.stts_slide = False
        self.lst_items = []
        self.cnt_totalitems = 0
        self.currentW = 0
        self.totalW = 0
        self.go = int
        self.stts_itemtype = 0
        self.stts_cntrl = False
        self.stts_itemlist = False
        self.stts_acttools = False
        self.stts_conj = False
        self.stts_viewermode = 0
        self.change_list_tpcs = False
        self.updt = bool
        self.tp = ''
        self.tmore = True
        self.auto_pronounce = False
        

        #self.gui()
        
        # ------------------------------------
        self.p_media.Hide()
        # ------------------------------------
        self.SetTitle(u'Idiomind - ' + self.tpc)
        
        if self.stts_topic != 20:
            self.stts_topictype = 0
            self.tab1 = u'Learning  ' + '(' + str(len(self.lst_learning)) +')'
            self.tab2 = u'Learned  ' + '(' + str(len(self.lst_learned)) +')'
            self.m_button14.SetLabel(u"Mark all as learnt")
            self.tab_practice.Enable()
        else:
            self.stts_topictype = 1
            self.tab1 = u'New items'
            self.tab2 = u'saved items'
            self.m_button14.SetLabel(u"Update")
            self.tab_practice.Disable()
        
        
            
        self.m_notebook1.SetPageText(2,self.tab1)
        self.m_notebook1.SetPageText(3,self.tab2)
        self.m_auiToolBar1.SetMargins(wx.Size(0,0))
        self.m_auiToolBar1.Realize()

        if self.stts_topic%2 != 1:
            # get playlist
            try:
                if self.stts_listmode == 0:
                    self.lst_items = self.lst_learning

                elif self.stts_listmode == 1:
                    self.lst_items = self.get_list_words()
                    
                elif self.stts_listmode == 2:
                    self.lst_items = self.get_sentences_lst()

                elif self.stts_listmode == 3:
                    self.lst_items = self.lst_marks
                    
                elif self.stts_listmode == 4:
                    self.lst_items = self.get_images_lst()
                    
                elif self.stts_listmode > 7:
                    tag = self.stts_listmode-7
                    self.lst_items = self.get_tag_lst(tag)

                self.chk_learning_lst.Clear()
                self.chk_learned_lst.Clear()
                self.chk_learning_lst.InsertItems(items=self.lst_learning, pos=0)
                self.chk_learned_lst.InsertItems(items=self.lst_learned, pos=0)
              
            except:
                pass
                
        elif self.stts_topic%2 == 1:
            self.chk_learned_lst.Clear()
            self.chk_learned_lst.InsertItems(items=self.lst_learned, pos=0)
        try:
            self.pract_on_start()
        except:
            pass
        
        
        self.active_tpc = self.tpc
        self.m_button111.Enable(False)
        self.show_topic_info()
        
        self.Layout()
        
        self.watcher.Start(5000)
        self.stts_firsttime = False
        #self.s_changes.Stop()
        
    # ===============================
    def overview_load(self):
        self.t_lst.ClearAll()
        self.il = wx.ImageList(42, 42)
        self.t_lst.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.t_lst.InsertColumn(0, '')
        self.t_lst.SetColumnWidth(0, 350)
        dimg = '/usr/share/sniparse/images/'
        
        if not os.path.exists(self.fl_jsn):
            with open(self.fl_jsn, 'wb') as index:
                json.dump({'own': [], 'fd': [], 'itll': [], 'tpcs': []}, index, indent=4)
            
        with open(self.fl_jsn, 'rb') as index:
            indx = json.load(index)
        self.lst_tpcs = indx['tpcs']

        for t in self.lst_tpcs:
            try:
                cnf = open(self.lng_dir + '/' + t + '/review.cfg').readlines()
            except:
                self.get_stts(t)
                
            cnf = cnf[0].strip()
            
            if len(cnf.split("|")) == 3:
                cnf = cnf.split("|")
                s = cnf[0].rstrip('\n')
                self.il.Add(wx.Bitmap(dimg + s))
            else:
                s = self.get_stts(t)
                self.il.Add(wx.Bitmap(dimg + str(s)))
            self.t_lst.InsertStringItem(0, t)
            self.t_lst.SetItemImage(0, self.lst_tpcs.index(t))

        
    def get_stts(self, t):
        try:
            print('i Error getting data, fix')
            from datetime import datetime, date
            d = datetime.utcnow().strftime("%Y-%m-%d")
            tdb = self.lng_dir + t + '/' + 'tpc'
            db = sqlite3.connect(tdb)
            cur = db.cursor()
            cur.execute("SELECT * FROM  Topic")
            flds = cur.fetchall()
            s = [i[9] for i in flds][0]
            stts = open(self.lng_dir + t + '/review.cfg','w')
            print >> stts, str(s%2)+'|'+str(s)+'|'+d
            return s
        except:
            pass

    
    def show_topic_info(self):
        self.count_sente = 'Sentences ' + str(len(self.lst_learning))
        self.count_words = 'Words ' + str(len(self.lst_learned))
        self.label_active_topic.SetLabel("  "+self.active_tpc)
        self.label_active_topic_info1.SetLabel("   " + self.count_words + "  " + self.count_sente + " ")
        self.label_active_topic_info2.SetLabel("   "+self.active_tpc)
        

    #############################################################################3
    #############################################################################3
    # ----------------------------
    def dprocess(self, d0, d1):
        d0 = self.datetime.strptime(d0, "%Y-%m-%d")
        d1 = self.datetime.strptime(d1, "%Y-%m-%d")
        return abs((d0 - d1).days)

    # ----------------------------
    def set_review(self):
        if self.stts_topic%2 != 0:
            self.datetime = datetime
            d0 = datetime.utcnow().strftime("%Y-%m-%d")
            cnf = open(self.tpc_dir + '/review.cfg').readlines()
            cnf = cnf[0].split("|")
            s = int(cnf[1].rstrip('\n'))
            d1 = cnf[2].rstrip('\n')
            days = int(self.dprocess(d0, d1))
            if self.stts_topic == 1 or self.stts_topic == 11:
                gc = days*100/15
            elif self.stts_topic == 3 or self.stts_topic == 13:
                gc = days*100/20
            elif self.stts_topic == 5 or self.stts_topic == 15:
                gc = days*100/30
            elif self.stts_topic == 7 or self.stts_topic == 17:
                gc = days*100/45
            elif self.stts_topic == 9 or self.stts_topic == 19:
                gc = days*100/60
            if gc > 100:
                gc = 100
            #self.dgauge.SetValue(gc)
            #self.t_review.SetLabel(u"ooelos de add uno con image grande y orto con pequeño tener dos modelos de add uno con image grande y orto con pequeño tener dos modelos de add uno con image grande y orto con pequeño")
            #self.t_review.Wrap(340)
            
            self.chk_learning_lst.Clear()
            self.tab_practice.Disable()
            self.tab_learning.Disable()
            self.tab_study.Disable()
            self.p_image.Hide()
            self.menuItem1.Enable(False)
            self.menuItem2.Enable(True)
            
        else:
            if self.stts_topic != 20:
                self.menuItem1.Enable(True)
                self.tab_practice.Enable()
            
            self.chk_learned_lst.Clear()
            
            self.tab_learning.Enable()
            self.tab_study.Enable()
            self.menuItem2.Enable(False)
    
    
    def changes_first_list(self, event):
        if self.stts_topic != 20:
            self.change_to_learnt(None)
        else:
            os.system("python /usr/share/sniparse/update_feeds.py &")
           
    
    def change_to_learnt(self, event):
        self.change_list_tpcs = True
        self.cnt_item = 0
        self.chk_learning_lst.Clear()
        self.chk_learned_lst.InsertItems(items=self.lst_learning, pos=0)
        stts = self.stts_topic + 1
        self.cur.execute('UPDATE Topic SET stts=? WHERE stts=?',
        (stts,self.stts_topic))
        dl="DELETE FROM Learning"
        self.cur.execute(dl)
        for item in self.lst_learning:
            self.cur.execute("insert into Learned values (?)",(item,))
            # items in practice boxs (all at box3 - learned)
            if len(item.split(' ')) == 1:
                for q in range(3):
                    for b in range(5):
                        dl = "DELETE FROM Q" + str(q) + "bx" + str(b) + " WHERE Items=?"
                        self.cur.execute(dl,(item,))
                    ins = "insert into Q" + str(q) + "bx4 values (?)"
                    self.cur.execute(ins,(item,))
            elif len(item.split(' ')) != 1:
                for b in range(5):
                    dl = "DELETE FROM Q3bx" + str(b) + " WHERE Items=?"
                    self.cur.execute(dl,(item,))
                ins = "insert into Q3bx4 values (?)"
                self.cur.execute(ins,(item,))

        self.db.commit()
        Learning = self.cur.fetchall()
        
        self.menuItem1.Enable(False)
        self.menuItem2.Enable(True)
        self.tab_practice.Disable()
        self.tab_learning.Disable()
        self.tab_study.Disable()
        self.p_image.Hide()

        d = datetime.utcnow().strftime("%Y-%m-%d")
        f = open(self.tpc_dir + '/review.cfg','w')
        print >> f, '1|'+str(stts)+'|'+d
        
        self.load()
        
    
    def change_to_learn(self, event):
        self.change_list_tpcs = True
        self.chk_learned_lst.Clear()
        self.chk_learning_lst.InsertItems(items=self.lst_learned, pos=0)
        stts = self.stts_topic + 1
        self.cur.execute('UPDATE Topic SET stts=? WHERE stts=?',
        (stts,self.stts_topic))
        
        dl="DELETE FROM Learned"
        self.cur.execute(dl)
        
        self.cur.execute("select trgt from Sentences")
        sntncs = self.cur.fetchall()
        sntncs = [i[0] for i in sntncs]
        self.cur.execute("select trgt from Words")
        wrds = self.cur.fetchall()
        wrds = [i[0] for i in wrds]
        self.cur.execute("select Items from Items")
        items = self.cur.fetchall()
        items = [i[0] for i in items]
        
        for item in items:
            self.cur.execute("insert into Learning values (?)",(item,))

        # remove all list in practice
        for q in range(4):
            for b in range(5):
                dl = "DELETE FROM Q" + str(q) + "bx" + str(b)
                self.cur.execute(dl)
        # restart sentences list in practice (to box 0)
        for item in sntncs:
            ins = "insert into Q3bx0 values (?)"
            self.cur.execute(ins,(item,))
        # restart words list in practice (to box 0)
        for item in wrds:
            for q in range(3):
                ins = "insert into Q" + str(q) + "bx0 values (?)"
                self.cur.execute(ins,(item,))
        self.db.commit()
        for x in range(4):
            self.pract_set_stats(x)
        Learning = self.cur.fetchall()

        self.menuItem2.Enable(False)
        self.menuItem1.Enable(True)
        self.tab_practice.Enable()
        self.tab_learning.Enable()
        self.tab_study.Enable()
        
        d = datetime.utcnow().strftime("%Y-%m-%d")
        f = open(self.tpc_dir + '/review.cfg','w')
        print >> f, '0|'+str(stts)+'|'+d

        self.load()
        self.update_items(self.lst_items, self.cnt_item)


    def content_refresh(self, event):
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        w_lst = [i[0] for i in Learning]
        self.Config.read(self.cfgfile)
        w_tpc = self.Config.get("Topic", "Name")
        if self.stts_itemlist == True or self.tpc != w_tpc or len(self.lst_learning) != len(w_lst):
            
            print('Refresh...')
            if self.change_list_tpcs == True:
                self.t_lst.ClearAll()
                self.overview_load()
            
            self.load()
            for x in range(4):
                self.pract_set_stats(x)
                
            self.change_toolBarSize(event)
            self.update_items(self.lst_items, self.cnt_item)
            
        else:
            pass
    
    
    def load_item(self, cnt_item):
        try:
            self.item = self.lst_items[cnt_item]
                    # check_data if note is mark for set icon
            if self.item in self.lst_marks:
                self.item_mark = True
            else:
                self.item_mark = False
            # check_data topic tipe for set icon in screen
            if self.stts_topictype == 0:
                pass
            elif self.stts_topictype == 1:
                if self.stts_changelist == True:
                    pass
                else:
                    if self.item in self.lst_learned:
                        self.stts_changelist = True
                    else:
                        self.stts_changelist = False
            # If is a word
            if len(self.item.split(' ')) == 1:
                self.stts_itemtype = 0
                self.load_type_word(self.item)
            # Is is a sentence
            elif len(self.item.split(' ')) != 1:
                self.stts_itemtype = 1
                self.load_type_sentence(self.item)
        except:
            self.html_field.SetPage('<br /><br /><font size="1" color="#3E3E3E">&nbsp;&nbsp;&nbsp; Not items</font><br /><br />')
            pass


    
    
    def load_type_word(self, item):
        self.item = item
        #self.words_list.Hide()
        flds = "SELECT * FROM Words WHERE trgt=?"
        self.cur.execute(flds, [(self.item)])
        flds = self.cur.fetchall()
        id_media = [i[5] for i in flds][0]
        self.img = [i[6] for i in flds][0]
        self.trgt = [i[0] for i in flds][0]
        self.srce = [i[2] for i in flds][0]
        expl = [i[3] for i in flds][0]
        self.expl = expl.replace(self.trgt.lower(), 
        '<b>' + self.trgt.lower() + '</b>')
        self.defn = [i[4] for i in flds][0]
        self.note = [i[7] for i in flds][0]
        self.note1 = [i[10] for i in flds][0]
        self.note2 = [i[11] for i in flds][0]
        self.noteimg = [i[12] for i in flds][0]
        self.ilink = [i[13] for i in flds][0]
        self.f1 = [i[8] for i in flds][0]
        self.f2 = [i[9] for i in flds][0]
        self.audio = self.tpc_dir + '/' + id_media + '.mp3'
        self.image = self.lng_dir + "/.share/images/" + self.trgt.lower() + '-0.jpg'

        if not os.path.exists(self.image) and self.stts_viewimg == True:
            
            if self.go == 1: #saltar si no exste imagen
                self.move_next_item()
            else:
                self.move_previous_item()
        else:
            if os.path.exists(self.image):
                #if not self.trgt in self.lst_images:
                    #self.cur.execute("insert into Images values (?)",(self.trgt,))
                    #self.db.commit()
                if self.stts_viewimg == False:
                    img = wx.Image(self.image)
                    img.Rescale(280, 190)
                    img = wx.BitmapFromImage(img)
                    self.i = img
                    self.img_item.SetBitmap(self.i)
                    self.p_image.Show()
                else:
                    #self.b_open.Enable(False)
                    self.img_item.Hide()
                    self.p_html.Hide()
                    self.large_img_item.Show()
                    w = self.p_bimage.GetSize()
                    img = wx.Image(self.image)
                    img.Rescale(w[0], w[1])
                    img = wx.BitmapFromImage(img)
                    self.i = img
                    self.large_img_item.SetBitmap(self.i)
            else:
                #if self.trgt in self.lst_images:
                    #self.cur.execute("delete from Images values (?)",(self.trgt,))
                    #self.db.commit()
                self.p_image.Hide()
                self.large_img_item.Hide()
            if self.f1 == 6:
                pass
                #self.b_open.Enable(True)
                #self.radioBox.Hide()
            elif self.f1 != 6:
                pass
                #self.b_open.Enable(False)
                #self.radioBox1.Hide()
                #self.radioBox.Hide()
            page = scrnHtml.word(self.trgt, self.srce, self.expl, self.note1,
             self.note2, self.item_mark, self.stts_changelist, self.stts_topictype, self.stts_acttools)
            self.html_field.SetPage(page)

            self.html_field.SetBackgroundColour(self.c_bgcolor)
            
            
        
            self.tab_study.Layout()
            #self.label_img.SetLabel(self.noteimg)
            self.stts_changelist = False
    
    
    def load_type_sentence(self, item):
        self.item = item
        global flds

        #self.radioBox1.Hide()
        self.cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(self.item)])
        flds = self.cur.fetchall()
        id_media = [i[12] for i in flds][0]
        self.img = [i[13] for i in flds][0]
        self.trgt = [i[0] for i in flds][0]
        self.srce = [i[9] for i in flds][0]
        twrds = [i[10] for i in flds][0]
        swrds = [i[11] for i in flds][0]
        self.mrk = [i[8] for i in flds][0]
        self.note1 = [i[15] for i in flds][0]
        self.note2 = [i[16] for i in flds][0]
        self.noteimg = [i[17] for i in flds][0]
        self.ilink = [i[18] for i in flds][0]
        self.audio = self.tpc_dir + '/' + id_media + '.mp3'
        self.image = self.tpc_dir + '/' + id_media + '.jpg'
        self.audio_attachmt = self.tpc_dir + '/' + id_media + '_l.mp3'
        

        #self.rtc.Clear()
        #self.rtc.SetDelayedLayoutThreshold(2)

        #self.rtc.BeginAlignment(rt.TEXT_ALIGNMENT_LEFT)


        #self.rtc.BeginFontSize(12)
        #self.rtc.BeginParagraphSpacing(0, 20)
        #self.rtc.WriteText(self.note1)
        #self.rtc.EndFontSize()


        #self.rtc.EndParagraphSpacing()
        
        #self.b_svmrk = False
        #if self.mrk == 0:
            #self.chkgrmt = 0
            #if self.stts_hlgrammar !=0:
                #self.mrk = self.stts_hlgrammar
        #else:
            #self.b_svmrk.SetValue(True)
        self.trgt = [i[self.stts_hlgrammar] for i in flds][0]

        #if not os.path.exists(self.image) and self.stts_viewimg == True:
            #if self.go == 1: #saltar si no exste imagen
                #self.move_next_item()
            #else:
                #self.move_previous_item()
            #pass
            
        #else:
        if os.path.exists(self.image) or os.path.exists(self.audio_attachmt):
            if os.path.exists(self.image):
                #if not self.trgt in self.lst_images:
                    #self.cur.execute("insert into Images values (?)",(self.trgt,))
                    #self.db.commit()
                img = wx.Image(self.image) 
                img.Rescale(280, 190) 
                img = wx.BitmapFromImage(img) 
                
                if self.stts_viewimg == False:
                    #self.b_open.Enable(True)
                    self.i = img
                    self.img_item.SetBitmap(self.i)
                else:
                    #self.b_open.Enable(False)
                    w = self.p_bimage.GetSize()
                    self.img_item.Hide()
                    self.p_html.Hide()
                    img = wx.Image(self.image) 
                    img.Rescale(w[0], w[1])
                    img = wx.BitmapFromImage(img) 
                    self.i = img
                    self.large_img_item.SetBitmap(self.i)
                    self.large_img_item.Show()
                    
            elif os.path.exists(self.audio_attachmt):
                if not os.path.exists(self.image):
                    from mutagen import File
                    try:
                        file = File(self.audio_attachmt)
                        artwork = file.tags['APIC:'].data
                        with open('/tmp/.img.jpg', 'wb') as img:
                            img.write(artwork)
                        imp = '/tmp/.img.jpg'
                    except:
                        imp = "/usr/share/sniparse/images/audio_podcast.png"
                    img = wx.Image(imp)
                    img.Rescale(280, 190)
                    img = wx.BitmapFromImage(img)
                    self.img_item.SetBitmap(img)
                    
                self.b_play_enc.SetLabel('Stop')
                self.b_play_enc.SetBitmapLabel(wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU))
                self.p_media.Show()
            else:
                #if self.trgt in self.lst_images:
                    #self.cur.execute("delete from Images values (?)",(self.trgt,))
                    #self.db.commit()
                self.p_media.Hide()
            self.p_image.Show()
        else:
            self.p_image.Hide()
            self.large_img_item.Hide()


        twrds = [x.encode('utf-8') for x in twrds.splitlines()]
        swrds = [x.encode('utf-8') for x in swrds.splitlines()]
        #self.words_list.DeleteAllItems()
        #index = 0
        #while index < len(twrds):
            #t = twrds[index].strip()
            #s = swrds[index].strip()
            #self.words_list.InsertStringItem(index, t)
            #self.words_list.SetStringItem(index, 1, s)
            #index += 1

        page = scrnHtml.sentence(self.trgt, self.srce, self.note1, 
        self.item_mark, self.stts_changelist, self.stts_hlgrammar, 
        self.stts_topictype, id_media, self.stts_acttools)
        self.html_field.SetPage(page)
        self.html_field.SetBackgroundColour(self.c_bgcolor)
        self.tab_study.Layout()
        
        
        
        #self.label_img.SetLabel(self.noteimg)
        #self.label_img.Wrap(220)
        self.stts_changelist = False
        #self.radioBox.SetSelection(self.mrk)
        
    
    def get_list_words(self):
        self.cur.execute("select trgt from Sentences")
        Sentences = self.cur.fetchall()
        lst_sentences = [i[0] for i in Sentences]
        if len(lst_sentences) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, lst_sentences))
            p = re.compile(p)
            words = [i for i in self.lst_learning if not p.search(i)]
            self.cnt_words = len(words)
            return words
        else:
            self.cur.execute("select trgt from Words")
            words = self.cur.fetchall()
            words = [i[0] for i in words]
            self.cnt_words = len(words)
            return words
    
    def get_sentences_lst(self):
        self.cur.execute("select trgt from Words")
        Words = self.cur.fetchall()
        lst_words = [i[0] for i in Words]
        if len(lst_words) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, lst_words))
            p = re.compile(p)
            sentences = [i for i in self.lst_learning if not p.search(i)]
            self.cnt_sentences = len(sentences)
            return sentences
        else:
            self.cur.execute("select trgt from Sentences")
            sentences = self.cur.fetchall()
            self.cnt_sentences = len(sentences)
            sentences = [i[0] for i in sentences]
            return sentences
            
    def get_images_lst(self):
        self.cur.execute("select Items from Images")
        Images = self.cur.fetchall()
        lst_Images = [i[0] for i in Images]
        images = [i for i in lst_Images if self.lst_learning]
        self.cnt_Images = len(images)
        return images

    # tags
    # -----------------------------------------------
    def get_tags_lst(self):
        self.cur.execute("PRAGMA table_info('tags')")
        tags = self.cur.fetchall()
        self.lst_tags = [i[1] for i in tags]
        self.cnt_tags = len(self.lst_tags)
        
    def get_tag_lst(self, tag):
        print(self.lst_tags)
        print(tag)
        print (self.lst_tags[tag])
        
        # GET list of espesific tag (wich store in db and convert to list then) | for save and play it
        flds = "SELECT "+self.lst_tags[tag]+" FROM tags"

        self.cur.execute(flds)
        lst_tag = self.cur.fetchall()
        try:
            lst = []
            for item in str(lst_tag[0][0]).split(":"):
                lst.append(item)
            self.lst_tag = lst
        except:
            self.lst_tag = []
        return self.lst_tag
        
    def create_tag(self, name):
        self.cur.execute("alter table tags add column '%s' 'TEXT'" % name)
        self.db.commit()
        
    def save_tag(self, tag, add, item):
        # get fron database especific tag
        flds = "SELECT "+self.lst_tags[tag]+" FROM tags"
        self.cur.execute(flds)
        lst_tag = self.cur.fetchall()
        lst_tag = [i[0] for i in lst_tag]
        # conver string to list
        try:
            lst = []
            for item in str(lst_tag[0][0]).split(":"):
                lst.append(item)
            lst_tag = lst
        except:
            lst_tag = []
        # insert or remove item fron tags list
        if add is True:
            lst_tag.append(item)
        else:
            try:
                lst_tag.remove(item)
            except:
                pass
        # declare tag list 
        self.lst_tag = lst_tag
        # conver list to a string
        str_list = ""
        for item in self.lst_tag:
            str_list += "{}:".format(item)
        lst_tag_to_save = str_list[:-1]
        # delete and update
        self.cur.execute("delete from tags").rowcount, self.lst_tags[tag]
        self.cur.execute("insert into tags("+self.lst_tags[tag]+") values (?)", (lst_tag_to_save,))
        self.db.commit()

    # list to show
    
    def Mode(self, idmd):
        self.stts_listmode = idmd
        self.stts_viewimg = True
        self.switch_view_img(None)
        
        if idmd == 0:
            self.cnt_all = len(self.lst_learning)
            self.lst_items = self.lst_learning

        elif idmd == 1:
            self.lst_items = self.get_list_words()

        elif idmd == 2:
            self.lst_items = self.get_sentences_lst() 

        elif idmd == 3:
            self.cnt_marks = len(self.lst_marks)
            self.lst_items = self.lst_marks
        
        elif idmd == 4:
            self.lst_items = self.get_images_lst()
            
        elif idmd > 7:
            tag = idmd-7
            self.lst_items = self.get_tag_lst(tag)
           
        if len(self.lst_items) == 0:
            self.html_field.SetPage('<br /><br /><font size="3" color="#3E3E3E">&nbsp;&nbsp;&nbsp; Not items</font><br /><br />')
            self.updt = False
            pass
        else:
            self.updt = True
            self.cnt_item = 0
            self.update_items(self.lst_items, self.cnt_item)
    
    # big image
    
    def switch_view_img(self, event):
        self.tab_study.Layout()
        if self.stts_viewimg == False:
            self.stts_viewimg = True
            #self.b_open.Enable(False)
            self.img_item.Hide()
            self.p_html.Hide()
            w = self.p_html.GetSize()
            if os.path.exists(self.image):
                img = wx.Image(self.image) 
                img.Rescale(w[0], w[1])
                img = wx.BitmapFromImage(img) 
                self.i = img
                self.large_img_item.SetBitmap(self.i)
                self.p_bimage.Show()
                self.large_img_item.Show()
                self.tab_study.Layout()
            else:
                self.tab_study.Layout()
        else:
            self.stts_viewimg = False
            #self.b_open.Enable(True)
            self.p_bimage.Hide()
            self.tab_study.Layout()
            if os.path.exists(self.image):
                self.p_html.Show()
                self.img_item.Show()
                img = wx.Image(self.image) 
                img.Rescale(280, 190)
                img = wx.BitmapFromImage(img)
                self.i = img
                self.img_item.SetBitmap(self.i)
            self.tab_study.Layout()
        #event.Skip()
    
    ## -----------------
    #def onKeyPress(self, event):
        #keycode = event.GetKeyCode()
        #self.Next(event)
        #event.Skip()
    
    # Handle of slider bind with show items
    # -----------------
    #def load_this(self, event):
        #item = self.stts_slider.GetValue() - 1
        #self.item = self.lst_items[item]
        #if item < len(self.lst_items):
            #self.load_item(self.cnt_item)
            #self.cnt_item = item
        #elif item > len(self.lst_items):
            #self.load_item(self.cnt_item)
            #self.cnt_item = 0

    # Slide Show
    # -----------------
    def on_slideshow(self, event):
        if self.stts_slide == False:
            self.stts_slide = True
            os.environ['m'] = str(self.stts_listmode)
            if self.stts_slidemode == True:
                os.system('python /usr/share/sniparse/slide.py $m &')
                self.Destroy()
            else:
                pi = wx.ArtProvider.GetBitmap(u"gtk-media-stop", wx.ART_BUTTON)
                self.m_auiToolBar1.SetToolBitmap(2, pi)
                self.stime.Start(6000)
        else:
            self.stime.Stop()
            self.stts_slide = False
            pi = wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_BUTTON)
            self.m_auiToolBar1.SetToolBitmap(2, pi)

    # -----------------
    def play_slide(self, event):
        self.move_next_item()
        self.pronounce_sleep()

    # -----------------
    def Cslide(self, event):
        self.stts_slidemode = event.IsChecked()
        event.Skip()
    
    def finvert_color(self, event):
        if self.c_bgcolor == wx.Colour(255, 255, 255):
            self.c_bgcolor = wx.Colour(55, 55, 55)
        else:
            self.c_bgcolor = wx.Colour(255, 255, 255)
        self.html_field.SetBackgroundColour(self.c_bgcolor)
       

    # -----------------
    def move_item_marklist(self, item):
        
        if not item:
            item = self.item
            
        if not item in self.lst_marks:
            self.cur.execute("INSERT INTO Marks (Items) VALUES (?)", (item,))
        else:
            self.cur.execute('DELETE FROM Marks WHERE Items=?',(item,))
        self.db.commit()
        self.cur.execute("select Items from marks")
        marks = self.cur.fetchall()
        marks_lst = [i[0] for i in marks]
        self.lst_marks = marks_lst[::-1]
        self.update_items(self.lst_items, self.cnt_item)
        self.load_item(self.cnt_item)
        if self.stts_listmode == 3:
            self.lst_items = self.lst_marks

    # -----------------
    def check_data(self, item):
        if not item:
            item = self.item
        self.cnt_item = self.lst_items.index(item)
        self.watcher.Start(500)
        self.stts_itemlist = True
        # if topic is a normal type
        if self.stts_topictype == 0:
            self.stts_changelist = True
            self.cur.execute('DELETE FROM Learning WHERE Items=?',(item,))
            self.cur.execute("insert into Learned values (?)",(item,))
            # items in practice boxs
            if self.stts_itemtype == 0:
                for q in range(3):
                    for b in range(5):
                        dl = "DELETE FROM Q" + str(q) + "bx" + str(b) + " WHERE Items=?"
                        self.cur.execute(dl,(item,))
                    ins = "insert into Q" + str(q) + "bx4 values (?)"
                    self.cur.execute(ins,(item,))
            elif self.stts_itemtype == 1:
                for b in range(5):
                    dl = "DELETE FROM Q3bx" + str(b) + " WHERE Items=?"
                    self.cur.execute(dl,(item,))
                ins = "insert into Q3bx4 values (?)"
                self.cur.execute(ins,(item,))
            # check_data if list marks items is active currently
            if self.stts_listmode == 3:
                self.cur.execute('DELETE FROM Marks WHERE Items=?',(item,))
                self.cur.execute("select Items from marks")
                marks = self.cur.fetchall()
                marks_lst = [i[0] for i in marks]
                self.lst_marks = marks_lst[::-1]
            self.db.commit()
            self.cur.execute("select Items from Learning")
            Learning = self.cur.fetchall()
            self.lst_learning = [i[0] for i in Learning]
            self.lst_learning = self.lst_learning[::-1]
            # marks like learned?
            if len(self.lst_learning) > 0:
                if self.cnt_item > self.cnt_totalitems:
                    self.cnt_item = 0
                self.load_item(self.cnt_item)
                #self.stts_slider.SetValue(self.cnt_item)
            else:
                self.change_to_learnt(None)
        # if topic is a feed type
        elif self.stts_topictype == 1:
            if not item in self.lst_learned:
                self.stts_changelist = True
                self.cur.execute("insert into Learned values (?)",(item,))
            elif item in self.lst_learned:
                self.stts_changelist = False
                self.cur.execute('DELETE FROM Learned WHERE Items=?',(item,))
            self.db.commit()
            self.load_item(self.cnt_item)
            #self.stts_slider.SetValue(self.cnt_item)
        
    
    # conjugate system FIXED
    # -----------------
    def conjugate(self, event):
        Topic.forms = ['Present', 'Perfect', 'Past', 'Pluperfect', 'Future', 'Future perfect', 'Subjunctive Present', 'Subjunctive Perfect', 'Subjunctive Imperfect', 'Subjunctive Pluperfect', 'Conditional Present', 'Conditional Perfect', 'Continuous Indicatives Present', 'Continuous Indicatives Perfect', 'Continuous Indicatives Past', 'Continuous Indicatives Pluperfect', 'Continuous Indicatives Future', 'Continuous Indicatives Future perfect', 'Continuous Conditional Present', 'Continuous Conditional Perfect']
        dbc = sqlite3.connect('/usr/share/sniparse/ifs/vb_cj_v4.db')
        cur = dbc.cursor()
        index = 1
        self.cnjg = index
        if self.cnjg == 0:
            cur.execute("SELECT * FROM en1 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'I '
        elif self.cnjg == 1:
            cur.execute("SELECT * FROM en2 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'You '
        elif self.cnjg == 2:
            cur.execute("SELECT * FROM en3 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'He '
        elif self.cnjg == 3:
            cur.execute("SELECT * FROM en4 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'We '
        elif self.cnjg == 4:
            cur.execute("SELECT * FROM en5 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'You '
        elif self.cnjg == 5:
            cur.execute("SELECT * FROM en6 WHERE name=?", [(self.item)])
            cnjg = cur.fetchall()
            pro = 'They '
        cnjg = list(cnjg[0])
        Topic.pro = pro
        self.update_forms(cnjg)
        
    def load_form(self, verb, form):
        self.hg = self.forms[form]
        self.html_field.SetPage(scrnHtml.Conjugate(self.pro, verb, self.hg))

    def move_next_form(self):
        if self.currentW == self.totalW-1:
            self.currentW = 0
        else:
            self.currentW += 1
        self.load_form(self.picPaths[self.currentW], self.currentW)

    def move_previous_form(self):
        if self.currentW == 0:
            self.currentW = self.totalW - 1
        else:
            self.currentW -= 1
        self.load_form(self.picPaths[self.currentW], self.currentW)

    def update_forms(self, cnjg):
        self.picPaths = cnjg
        self.totalW = len(self.picPaths)
        self.load_form(self.item, 0)

    # -----------------
    def get_info(self, event):
        self.stts_conj = True
        self.conjugate(None)
        #self.sub_p_loadPage.Show()
        #self.p_html.Hide()
        #self.Layout()
        #self.gif_wait.Play()
        
        #self.m_animCtrl2.Show()
        #self.tab_study.Layout()
        #self.m_animCtrl2.Play()
        
        #self.html_field.LoadPage("http://www.google.com/")

        #self.sub_p_loadPage.Hide()
        #self.gif_wait.Stop()
        #self.p_html.Show()
        #self.Layout()
        
        #self.m_animCtrl2.Hide()
        self.tab_study.Layout()
        #self.m_animCtrl2.Stop()
        
   
        
    
    def chck_grammar(self):
        self.stts_hlgrammar = self.stts_hlgrammar + 1
        if self.stts_hlgrammar > 7:
            self.stts_hlgrammar = 0
        self.load_item(self.cnt_item)
        
    
    def chs_style(self, event):
        self.stts_fontstyle = self.stts_fontstyle + 1
        if self.stts_fontstyle > 4:
            self.stts_fontstyle = 0
        self.html_field.SetStandardFonts(size=self.stts_fontsize, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        self.load_item(self.cnt_item)

    
    def show_from_list(self, event):
        try:
            item = self.chk_learning_lst.GetStringSelection()
            self.cnt_item = self.lst_items.index(item)
            #self.stts_slider.SetValue(self.cnt_item)
            self.load_item(self.cnt_item)
            self.tab_learning.Hide()
            self.tab_learned.Hide()
            self.tab_overview.Hide()
            self.tab_practice.Hide()
            self.tab_study.Hide()
            self.tab_learned.Show()
            self.tab_overview.Show()
            self.tab_practice.Show()
            self.tab_learning.Show()
            self.tab_study.Show()
            self.Layout()
        except:
            if self.stts_listmode == 1:
                msg = "Words"
            elif self.stts_listmode == 2:
                msg = "Sentences"
            elif self.stts_listmode == 3:
                msg = "Notes Marks"
            elif self.stts_listmode == 4:
                msg = "Notes with images"
            elif self.stts_listmode < 7:
                msg = "tags"
            else:
                msg = "Notes"
            msg="This note not in " + msg + " list"
            title=''
            dlg = wx.MessageDialog(self,message=msg,
                caption=title,
                style=wx.OK|wx.ICON_INFORMATION
              )
            ID = dlg.ShowModal()
        
    def check_action(self, event):
        item = self.chk_learning_lst.GetStringSelection()
        self.check_data(item)

    def move_next_item(self):
        self.stts_acttools = False
        self.stts_changelist = False
        if self.cnt_item == self.cnt_totalitems-1:
            self.cnt_item = 0
        else:
            self.cnt_item += 1
        self.load_item(self.cnt_item)
        #self.stts_slider.SetValue(self.cnt_item)
        
    
    def move_previous_item(self):
        self.stts_acttools = False
        self.stts_changelist = False
        if self.cnt_item == 0:
            self.cnt_item = self.cnt_totalitems - 1
        else:
            self.cnt_item -= 1
        self.load_item(self.cnt_item)
        #self.stts_slider.SetValue(self.cnt_item)
        
    
    def update_items(self, items, cnt_item):
        try:
            self.lst_items = items
            self.cnt_totalitems = len(self.lst_items)
            if cnt_item > self.cnt_totalitems:
                self.cnt_item = 0
            else:
                self.cnt_item = cnt_item
            #self.stts_slider.SetMax(len(self.lst_items))
            #self.stts_slider.SetValue(self.cnt_item)
            self.load_item(self.cnt_item)
            #self.stts_slider.Show()
            self.b_next.Enable(True)
            self.b_previous.Enable(True)
            print('update...   \n\n\tnote:' + self.lst_items[0] + '\n\tnotes: ' + str(len(self.lst_items)) + '\n\tmode: ' + str(self.stts_listmode))
            self.updt = True
        except:
            try:
                self.cnt_all = len(self.lst_learning)
                self.lst_items = self.lst_learning
                self.cnt_totalitems = len(self.lst_items)
                #self.stts_slider.SetMax(self.cnt_totalitems)
                #self.stts_slider.SetValue(0)
                self.load_item(0)
                #self.stts_slider.Show()
                self.b_next.Enable(True)
                self.b_previous.Enable(True)
                self.stts_listmode = 0
                print('update...   \n\n\tnote:' + self.lst_items[0] + '\n\tnotes: ' + str(len(self.lst_items)) + '\n\tmode: ' + str(self.stts_listmode))
                self.updt = True
                
            except:
                self.p_image.Hide()
                self.large_img_item.Hide()
                #self.stts_slider.Hide()
                self.b_next.Enable(False)
                self.b_previous.Enable(False)
                self.tab_study.Layout()
                if len(self.lst_learned) > 0:
                    self.updt = False
                    self.html_field.SetPage("No items")
                else:
                    self.updt = False
                    self.html_field.SetPage(" ")
        
    
    def on_item_Selected1(self, event):
        count = event.m_itemIndex
        #item = self.words_list.GetItem(itemId=count, col=0)
        self.item = item.GetText()
        os.environ['item'] = self.item
        os.system ('/usr/share/sniparse/audio/pl "$item" &')

    def on_viewer_context(self, event):
        text = self.html_field.SelectionToText()
        if text:
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()
                self.popupID3 = wx.NewId()
                self.popupID4 = wx.NewId()
                #self.Bind(wx.EVT_MENU, self.addtag, id=self.popupID1)
                #self.Bind(wx.EVT_MENU, self.adi, id=self.popupID1)
            menu = wx.Menu()
            
            itemOne = menu.Append(self.popupID1, text)
            menu.AppendSeparator()

            item = wx.MenuItem(menu, self.popupID1,"One")
            item.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU))
            menu.AppendItem(item)

            item = wx.MenuItem(menu, self.popupID2,"Info")
            item.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-info", wx.ART_MENU))
            menu.AppendItem(item)

            item = wx.MenuItem(menu, self.popupID3,"Add to Topic")
            item.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-add", wx.ART_MENU))
            menu.AppendItem(item)

            item = wx.MenuItem(menu, self.popupID4,"Mark")
            item.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-add", wx.ART_MENU))
            menu.AppendItem(item)

            self.PopupMenu(menu)
            menu.Destroy()
        else:
            pass


    def adi(self, event):
        self.m_animCtrl2.Show()
        self.tab_study.Layout()
        self.m_animCtrl2.Play()
        event.Skip()
        
    
    def f_Add(self, event):
        event.Skip()
        import add
        new_word = add.Add(self)
        new_word.Adding(self.item, '', self.trgt, '', '', self.tpc)
        #time.sleep(0.2)
        #self.m_animCtrl2.Hide()
        #self.m_animCtrl2.Stop()
        #self.Layout()

    
    def On_close(self, event):
        event.Skip(True)
        sz = self.GetSize()
        px = list(self.GetScreenPosition())
        Config = ConfigParser.ConfigParser()
        self.Config.read(self.cfgfile)
        self.Config.set('misc', 'pgrm', self.stts_hlgrammar)
        self.Config.set('misc', 'slide', self.stts_slidemode)
        self.Config.set('misc', 'fontStyle', self.stts_fontstyle)
        self.Config.set('misc', 'fontSize', self.stts_fontsize)
        self.Config.set('misc', 'showslider', self.stts_sslider)
        self.Config.set('misc', 'showpanel', self.stts_spanel)
        self.Config.set('misc', 'modeList', self.stts_listmode)
        self.Config.set('pos', 'w1', sz[0])
        self.Config.set('pos', 'h1', sz[1]-28)
        self.Config.set('pos', 'x2', px[0])
        self.Config.set('pos', 'y2', px[1]-28)
        cfgwrt = open(self.cfgfile,'w')
        self.Config.write(cfgwrt)
        cfgwrt.close()

        # Items list 1
        new_list = list(self.chk_learning_lst.GetCheckedStrings())
        for item in new_list:
            if not any(str(item) in s for s in self.lst_learned):
                self.cur.execute('DELETE FROM Learning WHERE Items=?',(item,))
                self.cur.execute("insert into Learned values (?)",(item,))
                
            # items in practice boxs
            #if len(item.split(' ')) == 1:
                #for q in range(3):
                    #for b in range(5):
                        #dl = "DELETE FROM Q" + str(q) + "bx" + str(b) + " WHERE Items=?"
                        #self.cur.execute(dl,(item,))
                    #ins = "insert into Q" + str(q) + "bx4 values (?)"
                    #self.cur.execute(ins,(item,))
            #elif len(item.split(' ')) != 1:
                #for b in range(5):
                    #dl = "DELETE FROM Q3bx" + str(b) + " WHERE Items=?"
                    #self.cur.execute(dl,(item,))
                #ins = "insert into Q3bx4 values (?)"
                #self.cur.execute(ins,(item,))


        ##Items list 2
        #new_list = list(self.chk_learned_lst.GetCheckedStrings())
        #for row in new_list:
            #if not any(str(row) in s for s in self.lst_learning):
                #self.cur.execute('DELETE FROM Learned WHERE Items=?',(row,))
                #self.cur.execute("insert into Learning values (?)",(row,))
                
        
        
        #self.cur.execute("insert into Topic values (?)",(row,))
        
        # Record and close 'db'
        
        self.db.commit()
        #self.db.close()
        self.Destroy()

    
    def pronounce(self):
        if os.path.exists(self.audio):
            os.environ['file'] = self.audio
            print(self.audio)
            os.system('(if ps -A | pgrep -f "play"; then killall play; fi; play  "$file") &')
            
        elif os.path.exists(self.lng_dir + "/.share/audio/" + self.trgt.lower() + ".mp3"):
            os.environ['file'] = self.lng_dir + "/.share/audio/" + self.trgt.lower() + ".mp3"
            os.system('(if ps -A | pgrep -f "play"; then killall play; fi; play  "$file") &')
            print(self.audio)
        else:
            pass
            

    def pronounce_sleep(self):
        if os.path.exists(self.audio):
            os.environ['file'] = self.audio
            os.system('(if ps -A | pgrep -f "play"; then killall play; fi; sleep 0.5; play  "$file") &')
            
        elif os.path.exists(self.lng_dir + "/.share/audio/" + self.trgt.lower() + ".mp3"):
            os.environ['file'] = self.lng_dir + "/.share/audio/" + self.trgt.lower() + ".mp3"
            os.system('(if ps -A | pgrep -f "play"; then killall play; fi; sleep 0.5; play  "$file") &')
        else:
            pass

    
    def show_dialog_config(self, event):
        from cnfg import CnfigDlg
        CnfigDlg = CnfigDlg(self)
        CnfigDlg.Show()

    
    def show_panel_info(self, event):
        os.system("'/usr/share/sniparse/ifs/info.py' &")
        event.Skip()

    def pract_swich_type(self, p, rstrt):
        self.labelq_0.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        self.labelq_1.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        self.labelq_2.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        self.labelq_3.SetFont(wx.Font(7, 70, 90, 90, False, wx.EmptyString))
        self.Qrestartf.Hide()
        self.QlistBox.Hide()
        self.Q_btn_ok.Hide()
        self.Q_btn_no.Hide()
        self.Q_btn_end.Hide()
        self.Q_btn_ok2.Hide()
        self.Q_btn_next4.Hide()
        self.Q_btn_play3.Hide()
        self.Qctext.Hide()
        self.Q_btn_show.Hide()
        if p == 0:
            self.Q_number = 0
        elif p == 1:
            self.Q_number = 1
        elif p == 2:
            self.Q_number = 2
        elif p == 3:
            self.Q_number = 3
        if rstrt == False:

            self.session = []
            self.Q_cItem = 0
            self.totalpItems = 0
            self.back = 0
            self.src_r = 0
            self.src_w = 0
            self.round2 = []
            self.fromBox = 0
            self.r = 1
            self.Q_ccItem = 0
            self.Qgauge.Show()
            self.Qgauge.SetValue(0)
        self.Panel_practice_2.Layout()
        
    # Q0
    # -------------------------------------------
    def pract_type_0(self, parent):
        self.box = dict()
        for n in range(5):
            exe = "select Items from Q0bx" + str(n)
            self.cur.execute(exe)
            b = self.cur.fetchall()
            self.box[n] = [i[0] for i in b]
            
        bx0 = self.box[0] * 4
        bx1 = self.box[1] * 3
        bx2 = self.box[2] * 2
        bx3 = self.box[3]
        bx4 = self.box[4]
        cnt = len(bx0 + bx1 + bx2 + bx3)
        
        if cnt == 0 and len(bx4) != 0:
            self.pract_swich_type(0, True)
            self.Qrestartf.Show()
            self.Panel_practice_2.Layout()
            self.QWHtml.SetPage(scrnHtml.Qokcnt(''))
        elif cnt > 0:
            self.pract_swich_type(0, False)
            # get the 20 elements that most are repeated in the 5 change_list
            if cnt/9 > 100:
                cnt9 = 100
            elif cnt/9 < 20:
                cnt9 = cnt
            else:
                cnt9 = cnt
            self.session = [self.Q_item for self.Q_item,count in Counter(bx0 + bx1 + bx2 + bx3).most_common(cnt9)]
            # mixing elements obtained
            shuffle(self.session)
            self.total = len(self.session)
            self.labelq_0.SetFont(wx.Font(7, 70, 90, 92, False, wx.EmptyString))
            self.top_info.SetLabel('Wrong 0  /  Well 0  - Remain ' + str(len(self.session)))
            self.imgbl = wx.Image('/usr/share/sniparse/images/bl.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.QWHtml.SetStandardFonts(size=self.Qsixe_font, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
            self.pract_update_items(self.session)
            self.Qgauge.SetRange(self.total)
        else:
            self.QWHtml.SetPage(scrnHtml.Qnocnt(''))
        
    # Q0
    def pract_show_item_0(self, Q0_item):
        self.pract_set_labelvalue()
        self.Q_btn_show.Show()
        self.Q_btn_no.Hide()
        self.Q_btn_ok.Hide()
        self.Panel_practice_2.Layout()
        global srce
        global trgt
        global imge
        self.Q_item = Q0_item
        self.pract_change_box(self.Q_item)
        flds = "SELECT * FROM Words WHERE trgt=?"
        self.cur.execute(flds, [(self.Q_item)])
        flds = self.cur.fetchall()
        md = [i[5] for i in flds][0]
        trgt = [i[0] for i in flds][0]
        srce = [i[2] for i in flds][0]
        self.QWHtml.SetPage(scrnHtml.FlashcardsA(trgt, srce))
        self.QWHtml.SetBackgroundImage(self.Qimg)
        
        
    # Q0
    def pract_show_card_1(self):
        self.QWHtml.SetPage(scrnHtml.FlashcardsB(trgt, srce))
        self.QWHtml.SetBackgroundImage(self.Qimg)
    
    # Q1
    # -------------------------------------------
    def pract_type_1(self, parent):
        global srce_ranlst
        # use database for get words in source language
        # and build one randon list whit then
        # remove sentences of learning list
        self.cur.execute("select trgt from Sentences")
        Sentences = self.cur.fetchall()
        lst_sentences = [i[0] for i in Sentences]
        
        if len(lst_sentences) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, lst_sentences))
            p = re.compile(p)
            self.ran_lst = [i for i in self.lst_learning if not p.search(i)]
        else:
            self.ran_lst = self.lst_learning
        # get words 
        srce_ranlst = []
        for x in self.ran_lst:
            self.cur.execute("select srce from Words WHERE trgt=?", [(x)])
            sitm = self.cur.fetchall()
            srce_ranlst.append(sitm)
        # conver list of tuple in one list
        srce_ranlst = [i[0] for i in srce_ranlst]
        srce_ranlst = [i[0] for i in srce_ranlst]

        self.box = dict()
        for n in range(5):
            exe = "select Items from Q1bx" + str(n)
            self.cur.execute(exe)
            b = self.cur.fetchall()
            self.box[n] = [i[0] for i in b]

        # BOX 1 multiply for 5
        bx0 = self.box[0] * 4
        bx1 = self.box[1] * 3
        bx2 = self.box[2] * 2
        bx3 = self.box[3]
        bx4 = self.box[4]
        cnt = len(bx0 + bx1 + bx2 + bx3)
        if cnt == 0 and len(bx4) != 0:
            self.pract_swich_type(1, True)
            self.Qrestartf.Show()
            self.Panel_practice_2.Layout()
            self.QWHtml.SetPage(scrnHtml.Qokcnt(''))
        elif cnt > 1:
            self.pract_swich_type(1, False)
            # get the 20 elements that most are repeated in the 5 change_list
            cnt9 = cnt/9
            if cnt9 > 100:
                cnt9 = 100
            self.session = [self.Q_item for self.Q_item,count in Counter(bx0 + bx1 + bx2 + bx3).most_common(cnt9)]
            # mixing elements obtained
            shuffle(self.session)
            self.total = len(self.session)

            self.QlistBox.Show()
            self.Panel_practice_2.Layout()
            from collections import OrderedDict
            self.OrderedDict = OrderedDict
            self.labelq_1.SetFont(wx.Font(7, 70, 90, 92, False, wx.EmptyString))
            self.top_info.SetLabel('Wrong 0  /  Well 0  - Remain ' + str(len(self.session)))
            self.imgbl = wx.Image('/usr/share/sniparse/images/bl.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.QWHtml.SetStandardFonts(size=self.Qsixe_font, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
            self.pract_update_items(self.session)
            self.Qgauge.SetRange(self.total)
        else:
            self.QWHtml.SetPage(scrnHtml.Qnocnt(''))

    # Q1
    def pract_show_item_1(self, Q0_item):
        self.pract_set_labelvalue()
        global srce
        global trgt
        self.Q_item = Q0_item
        self.pract_change_box(self.Q_item)
        flds = "SELECT * FROM Words WHERE trgt=?"
        self.cur.execute(flds, [(self.Q_item)])
        flds = self.cur.fetchall()
        md = [i[5] for i in flds][0]
        trgt = [i[0] for i in flds][0]
        srce = [i[2] for i in flds][0]
        shuffle(srce_ranlst)
        rwrds = srce_ranlst[:4]
        rwrds.append(srce)
        shuffle(rwrds)
        rwrds = list(self.OrderedDict.fromkeys(rwrds))
        self.QlistBox.Clear()
        self.QlistBox.Set(rwrds)
        self.QWHtml.SetPage(scrnHtml.FlashcardsA(trgt, srce))
        self.QWHtml.SetBackgroundImage(self.Qimg)
        
    # Q1
    def pract_type1_myvalue(self, event):
        event.Skip()
        chk = self.QlistBox.GetSelection()
        Mych = self.QlistBox.GetString(chk)
        if Mych == '':
            pass
        elif Mych != srce:
            self.pract_value_no(event)
            
        elif Mych == srce:
            self.pract_value_ok(event)

    # Q2
    # -------------------------------------------
    def pract_type_2(self, event):
        self.box = dict()
        for n in range(5):
            exe = "select Items from Q2bx" + str(n)
            self.cur.execute(exe)
            b = self.cur.fetchall()
            self.box[n] = [i[0] for i in b]
            
        bx0 = self.box[0] * 4
        bx1 = self.box[1] * 3
        bx2 = self.box[2] * 2
        bx3 = self.box[3]
        bx4 = self.box[4]
        cnt = len(bx0 + bx1 + bx2 + bx3)
        if cnt == 0 and len(bx4) != 0:
            self.pract_swich_type(2, True)
            self.Qrestartf.Show()
            self.Panel_practice_2.Layout()
            self.QWHtml.SetPage(scrnHtml.Qokcnt(''))
        elif cnt > 1:
            self.pract_swich_type(2, False)
            # get the 20 elements that most are repeated in the 5 change_list
            cnt9 = cnt/9
            if cnt9 > 100:
                cnt9 = 100
            self.session = [self.Q_item for self.Q_item,count in Counter(bx0 + bx1 + bx2 + bx3).most_common(cnt9)]
            # mixing elements obtained
            shuffle(self.session)
            self.total = len(self.session)

            self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
            self.emoji='&nbsp;<a href="[%s]v"><img src="memory:img.png"/></a>&nbsp;'

            self.labelq_2.SetFont(wx.Font(7, 70, 90, 92, False, wx.EmptyString))
            self.top_info.SetLabel('Wrong 0  /  Well 0  - Remain ' + str(len(self.session)))
            self.QWHtml.SetStandardFonts(size=self.Qsixe_font, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
            self.pract_update_items(self.session)
            self.Qgauge.SetRange(self.total)
        else:
            self.QWHtml.SetPage(scrnHtml.Qnocnt(''))

    # Q2
    def pract_show_item_2(self, Q0_item):
        self.pract_set_labelvalue()
        self.Q_btn_show.Show()
        self.Q_btn_play3.Show()
        self.Q_btn_no.Hide()
        self.Q_btn_ok.Hide()
        self.Panel_practice_2.Layout()
        global srce
        global trgt
        global imge
        global ftrgt
        self.Q_item = Q0_item
        self.pract_change_box(self.Q_item)
        flds = "SELECT * FROM Words WHERE trgt=?"
        self.cur.execute(flds, [(self.Q_item)])
        flds = self.cur.fetchall()
        self.pm_id = [i[5] for i in flds][0]
        trgt = [i[0] for i in flds][0]
        self.ftrgt = [i[0] for i in flds][0]
        srce = [i[2] for i in flds][0]
        self.Qaud = trgt
        
        trgt = re.sub('[%s]' % ''.join(self.vowels), '&nbsp;<a href=[%s]v><img src="memory:img.png"/></a>&nbsp;', trgt)

        self.QWHtml.SetPage(scrnHtml.FlashcardsC(trgt, srce))
        self.QWHtml.SetBackgroundImage(self.Qimg)
        self.pract_pronounce(None)
        
    # Q2
    def pract_show_card_3(self):
        self.QWHtml.SetPage(scrnHtml.FlashcardsD(self.ftrgt, srce))
        self.QWHtml.SetBackgroundImage(self.Qimg)
            
    # Q3
    # -------------------------------------------
    def pract_type_3(self, event):
        self.box = dict()
        for n in range(5):
            exe = "select Items from Q3bx" + str(n)
            self.cur.execute(exe)
            b = self.cur.fetchall()
            self.box[n] = [i[0] for i in b]

        # BOX 1 multiply for 5
        bx0 = self.box[0] * 4
        bx1 = self.box[1] * 3
        bx2 = self.box[2] * 2
        bx3 = self.box[3]
        bx4 = self.box[4]
        cnt = len(bx0 + bx1 + bx2 + bx3)
        if cnt == 0 and len(bx4) != 0:
            self.pract_swich_type(3, True)
            self.Qrestartf.Show()
            self.Panel_practice_2.Layout()
            self.QWHtml.SetPage(scrnHtml.Qokcnt(''))
            self.QWHtml.SetBackgroundImage(self.Qimg)
        elif cnt > 1:
            self.pract_swich_type(3, False)
            cnt9 = cnt/9
            if cnt9 > 30:
                cnt9 = 30
            # get the 20 elements that most are repeated in the 5 change_list
            self.session = [self.Q_item for self.Q_item,count in Counter(bx0 + bx1 + bx2 + bx3).most_common(cnt9)]
            # mixing elements obtained
            shuffle(self.session)
            print(str(len(self.session)))
            self.total = len(self.session)
            self.labelq_3.SetFont(wx.Font(7, 70, 90, 92, False, wx.EmptyString))
            self.top_info.SetLabel('Wrong 0  /  Well 0  - Remain ' + str(len(self.session)))
            self.pract_update_items(self.session)
            self.Qgauge.SetRange(self.total)
        else:
            self.QWHtml.SetPage(scrnHtml.Qnocnt(''))
        self.QWHtml.SetStandardFonts(size=self.Qsixe_font2, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")

    # Q3
    def pract_show_item_3(self, Q0_item):
        self.pract_set_labelvalue()
        self.Q_btn_next4.Hide()
        self.Qctext.Show()
        self.Q_btn_play3.Show()
        self.Q_btn_ok2.Show()
        self.Panel_practice_2.Layout()
        global srce
        global trgt
        self.Q_item = Q0_item
        self.pract_change_box(self.Q_item)
        flds = "SELECT * FROM Sentences WHERE trgt=?"
        self.cur.execute(flds, [(self.Q_item)])
        flds = self.cur.fetchall()
        md = [i[12] for i in flds][0]
        trgt = [i[0] for i in flds][0]
        chk_trgt = [i[0] for i in flds][0]
        srce = [i[9] for i in flds][0]
        #self.Qaudio = self.tpc_dir + md + '.mp3'
        self.chk_trgt = re.sub(r'[^\w]', ' ', chk_trgt)
        trgt = trgt.title()
        trgt = re.sub(r'[^\w]', ' ', trgt)
        trgt = re.sub(" ", "::", trgt)
        sust = lambda tx: re.sub('[a-z]', '.', tx)
        trgt = sust(trgt)
        trgt = re.sub("::", "   &nbsp;&nbsp;&nbsp;", trgt)
        self.QWHtml.SetPage(scrnHtml.FlashcardsE(trgt))
        self.QWHtml.SetBackgroundImage(self.Qimg)
        self.pract_pronounce(None)
        
        
    # Q3
    def pract_nextitem(self, event):
        if s == 1:
            self.pract_value_ok(event)
        else:
            self.pract_value_no(event)
        event.Skip()

    # Q3
    def pract_check_value(self, event):
        chk = self.Qctext.GetValue()
        self.Qctext.Clear()
        self.chk_trgt = self.chk_trgt.lower()
        trgtQcheck1 = self.chk_trgt.split(" ")
        chk = chk.lower()
        trgtQcheck2 = chk.split(" ")
        chkn1 = len(trgtQcheck1)
        chkn2 = 0
        for w in trgtQcheck2:
            if w in trgtQcheck1:
                chkn2 = chkn2 + 1
                self.chk_trgt = self.chk_trgt.replace(w, '<font color="#59A449">' + w + '</font>')
        self.chk_trgt = self.chk_trgt.title()
        if chkn2 != 0:
            prct = chkn2 * 100 / chkn1
        else:
            prct = 0
        global s
        if prct > 80:
            s = 1
        else:
            s = 0
        self.Q_btn_ok2.Hide()
        self.Qctext.Hide()
        self.Q_btn_next4.Show()
        self.Panel_practice_2.Layout()
        self.QWHtml.SetPage(scrnHtml.FlashcardsF(self.chk_trgt, srce, prct))
        self.QWHtml.SetBackgroundImage(self.Qimg)
        event.Skip()

    # ----- COMMONS - Practices
    def pract_set_labelvalue(self):
        if self.r == 1:
            self.t = self.totalpItems - self.Q_cItem + self.src_w
        else:
            self.t = self.totalpItems - self.Q_cItem
            
        self.top_info.SetLabel('Wrong ' + str(self.src_w) + '  /  Well ' + str(self.src_r) + '  -  Remain ' + str(self.t))
        
    def pract_load_data(self):
        self.cur.execute("select trgt from Sentences")
        sntncs = self.cur.fetchall()
        lst = [i[0] for i in sntncs]
        if len(lst) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, lst))
            p = re.compile(p)
            self.l_lstw = [i for i in self.lst_learning if not p.search(i)]
        else:
            self.l_lstw = self.lst_learning
       
        self.cur.execute("select trgt from Words")
        wrds = self.cur.fetchall()
        lst = [i[0] for i in wrds]
        if len(lst) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, lst))
            p = re.compile(p)
            self.l_lsts = [i for i in self.lst_learning if not p.search(i)]
        else:
            self.l_lsts = self.lst_learning


    def pract_set_stats(self, q):
        quiz = " Q"+str(q)
        n = 4
        head = True
        while n > -1:
            box = "bx"+str(n)
            exe = "select Items from" + quiz + box
            self.cur.execute(exe)
            bx = self.cur.fetchall()
            bx = [i[0] for i in bx]
            sum = len(bx)
            if q == 3:
                self.l_lst = self.l_lsts
            else:
                self.l_lst = self.l_lstw
            if len(self.l_lst) != 0:
                np = 100*sum/len(self.l_lst) 
            else:
                np = 100*sum/1
            np = self.pract_tool_getvalue(np)
            if sum > 0 and head is True:
                head = False
                image = eval("c%s" % n + "1%s" % np)
            else:
                image = eval("c%s" % n + "0%s" % np)
            bm = self.pract_tool_convertimg(image)
            exec("self.Q" + str(q) + "_%s" % n + ".SetBitmap(bm)") in globals(), locals()
            n = n-1


    def pract_tool_convertimg(self, image):
        img = PyEmbeddedImage(image)
        img = img.GetImage()
        img = img.ConvertToBitmap()
        return img
        
    def pract_tool_getvalue(self, num):
        step = 10
        for x in range(10):
            if num < step+1:
                break
            step += 10
        return x
        
    def pract_update_items(self, session):
        self.session = session
        self.totalpItems = len(self.session)
        exec("self.pract_show_item_" + str(self.Q_number) + "(self.session[0])")
        
    def pract_pronounce(self, event):
        if os.path.exists(self.lng_dir + "/" + self.tpc + "/" + self.pm_id + ".mp3"):
            os.environ['file'] = self.lng_dir + "/" + self.tpc + "/" + self.pm_id + ".mp3"
            os.system('(sleep 0.5; play  "$file") &')
            
        elif os.path.exists(self.lng_dir + "/.share/audio/" + self.Qaud.lower() + ".mp3"):
            os.environ['file'] = self.lng_dir + "/.share/audio/" + self.Qaud.lower() + ".mp3"
            os.system('(sleep 0.5; play  "$file") &')

    def pract_change_box(self, Q0_item):
        self.Q_item = Q0_item
        if self.Q_item in self.box[0]:
            self.fromBox = 0
        elif self.Q_item in self.box[1]:
            self.fromBox = 1
        elif self.Q_item in self.box[2]:
            self.fromBox = 2
        elif self.Q_item in self.box[3]:
            self.fromBox = 3
        else:
            self.fromBox = 4
            
    def pract_value_ok(self, event):
        self.src_r = self.src_r + 1
        if self.fromBox == 4:
            toBox = 4
        else:
            toBox = self.fromBox + 1
        self.pract_change_posBox(self.Q_item, toBox)
        self.pract_next_item()
        self.Q_ccItem = self.Q_ccItem + 1
        self.Qgauge.SetValue(self.Q_ccItem)
        event.Skip()
    
    def pract_value_no(self, event):
        self.src_w = self.src_w + 1
        if self.fromBox == 0:
            toBox = 0
        else:
            toBox = self.fromBox - 1
        self.round2.append(self.Q_item)
        self.pract_change_posBox(self.Q_item, toBox)
        self.pract_next_item()
        if self.Q_ccItem > 0:
            self.Q_ccItem = self.Q_ccItem - 1
        self.Qgauge.SetValue(self.Q_ccItem)
        event.Skip()
        
    def pract_change_posBox(self, Q0_item, toBox):
        self.Q_item = Q0_item
        self.box[self.fromBox].remove(self.Q_item)
        self.box[toBox].append(self.Q_item)

    def pract_next_item(self):
        if self.Q_cItem == self.totalpItems-1:
            if len(self.round2) == 0:
                self.pract_on_end()
            else:
                if self.r == 2:
                    self.pract_on_end()
                else:
                    self.r = 2
                    self.pract_on_round2()
                    self.Q_cItem = 0
        else:
            self.Q_cItem += 1
            exec("self.pract_show_item_"+str(self.Q_number)+"(self.session[self.Q_cItem])")
        
    
    def pract_on_round2(self):
        self.session = self.round2
        shuffle(self.session)
        self.pract_update_items(self.session)
        self.round2 = []
        self.Refresh()
        
    def pract_change_layout(self, event):
        if self.Q_number == 0:
            self.pract_show_card_1()
        elif self.Q_number == 2:
            self.pract_show_card_3()
        self.Q_btn_show.Hide()
        self.Q_btn_play3.Hide()
        self.Q_btn_no.Show()
        self.Q_btn_ok.Show()
        self.Panel_practice_2.Layout()
        self.Layout()
        event.Skip()
        
    def pract_restart(self, event):
        exe = "select Items from Q" + str(self.Q_number) + "bx4"
        self.cur.execute(exe)
        b4 = self.cur.fetchall()
        self.box4 = [i[0] for i in b4]

        if len(self.lst_learned) > 0:
            p = "(?:%s)" % "|".join(map(re.escape, self.lst_learned))
            p = re.compile(p)
            self.box4 = [i for i in self.box4 if not p.search(i)]
        else:
            self.box4 = self.box4

        dl="DELETE FROM Q" + str(self.Q_number) + "bx4"
        self.cur.execute(dl)
        exe = "insert into Q" + str(self.Q_number) + "bx0 values (?)"
        for row in self.box4:
            self.cur.execute(exe,(row,))
        self.db.commit()

        self.QWHtml.SetPage(scrnHtml.QStart(info=''))
        self.top_info.SetLabel('Comienza a practicar eligiendo el tipo de test')
        #self.QWHtml.SetBackgroundColour(wx.NullColor)
        self.Qrestartf.Hide()
        self.pract_load_data()
        self.pract_set_stats(self.Q_number)
        self.panel_img.Layout()
        self.Panel_practice_2.Layout()
        event.Skip()
    
    def pract_on_end(self):
        self.QlistBox.Hide()
        self.Q_btn_ok2.Hide()
        self.Q_btn_play3.Hide()
        self.Q_btn_next4.Hide()
        self.Q_btn_no.Hide()
        self.Q_btn_ok.Hide()
        self.Q_btn_show.Hide()
        self.Q_btn_end.Show()
        self.Panel_practice_2.Layout()
        chk1 = self.box[0] + self.box[1] + self.box[2] + self.box[3]
        scr1 = len(self.box[0])
        scr2 = len(self.box[1])
        scr3 = len(self.box[2])
        scr4 = len(self.box[3])
        scr5 = len(self.box[4])
        if len(chk1) == 0:
            os.system('play "/usr/share/sniparse/ifs/end-1.mp3" &')
            img = wx.Image('/usr/share/sniparse/images/p_end2.png')
            z = self.QWHtml.GetSize()
            img.Rescale(z[0], z[1])
            img = wx.BitmapFromImage(img)
            self.p_end = img
            self.QWHtml.SetPage(scrnHtml.QEndA(self.src_r, self.src_w))
            self.QWHtml.SetBackgroundImage(self.img)
        else:
            self.src_w = self.total - self.src_r
            if self.src_r > self.src_w or self.src_r == self.src_w:
                c = True
            else:
                c = False
            img = wx.Image('/usr/share/sniparse/images/p_end1.png')
            z = self.QWHtml.GetSize()
            img.Rescale(z[0], z[1])
            img = wx.BitmapFromImage(img)
            self.p_end = img
            os.system('play "/usr/share/sniparse/ifs/end-2.mp3" &')
            self.top_info.SetLabel(u'\tYour Score is')
            self.QWHtml.SetPage(scrnHtml.QEndB(self.src_r, self.src_w, c))
            self.QWHtml.SetBackgroundImage(self.p_end)
    
    
    def pract_on_start(self):
        self.QWHtml.SetPage(scrnHtml.QStart(info=''))
        self.top_info.SetLabel('Comienza a practicar eligiendo el tipo de test')
        #self.QWHtml.SetBackgroundColour(wx.NullColor)

    def pract_on_close(self, event):
        self.Qgauge.Hide()
        self.Q_btn_end.Hide()
        self.Panel_practice_2.Layout()
        self.Qgauge.SetValue(0)
        self.pract_on_start()
        for n in range(5):
            dl = "DELETE FROM Q" + str(self.Q_number) + "bx" + str(n)
            self.cur.execute(dl)
            ins = "insert into Q" + str(self.Q_number) + "bx" + str(n) + " values (?)"
            for row in  self.box[n]:
                self.cur.execute(ins,(row,))
        self.db.commit()
        self.pract_load_data()
        self.pract_set_stats(self.Q_number)
        self.panel_img.Layout()
        event.Skip()
    
    def pract_set_label0(self, event):
        self.labelq_0.SetForegroundColour(wx.Colour(125, 125, 125))
    def pract_set_label1(self, event):
        self.labelq_1.SetForegroundColour(wx.Colour(125, 125, 125))
    def pract_set_label2(self, event):
        self.labelq_2.SetForegroundColour(wx.Colour(125, 125, 125))
    def pract_set_label3(self, event):
        self.labelq_3.SetForegroundColour(wx.Colour(125, 125, 125))
    def pract_set_label(self, event):
        self.labelq_0.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        self.labelq_1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        self.labelq_2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        self.labelq_3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        
    # edit
    
    def edit_item(self, event):
        if len(self.trgt.split(' ')) == 1:
            from edit import eword
            self.edit = eword(self, self.item, self.tpc)
            self.edit.Bind(wx.EVT_CLOSE, self.refresh_a)
            self.edit.Show()
            
        elif len(self.trgt.split(' ')) != 1:
            from edit import esntc
            self.edit = esntc(self, self.item, self.tpc)
            self.edit.Bind(wx.EVT_CLOSE, self.refresh_b)
            self.edit.Show()
    
    def refresh_a(self, event):
        item = self.edit.edit_trgt.GetLabel()
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        self.lst_learning = [i[0] for i in Learning]
        self.update_items(self.lst_learning, self.cnt_item)
        self.lst_items = self.lst_learning[::-1]
        if item in self.lst_items:
            self.load_item(self.cnt_item)
        else:
            self.refresh_c()
        self.Refresh()
        self.edit.Destroy()
     
    def refresh_b(self, event):
        item = self.edit.edit_trgt.GetValue()
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        self.lst_learning = [i[0] for i in Learning]
        self.update_items(self.lst_learning, self.cnt_item)
        self.lst_items = self.lst_learning[::-1]
        if item in self.lst_items:
            self.load_item(self.cnt_item)
        else:
            self.refresh_c()
        self.Refresh()
        self.edit.Destroy()
        
    
    def Next(self, event):
        self.go = 1
        if self.stts_cntrl == False:
            self.move_next_item()
        elif self.stts_cntrl == True:
            if self.stts_listmode == 2:
                self.move_next_item()
            else:
                self.move_next_form()
        
        if self.auto_pronounce == True:
            self.pronounce_sleep()
    
    def Previous(self, event):
        self.go = 2
        if self.stts_cntrl == False:
            self.move_previous_item()
        elif self.stts_cntrl == True:
            if self.stts_listmode == 2:
                self.move_previous_item()
            else:
                self.move_previous_form()
            
        if self.auto_pronounce == True:
            self.pronounce_sleep()
    
    def refresh_c(self):
        self.move_next_item()
        self.move_previous_item()

    def chng_cur2(self, event):
        wx.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        #self.labelq_0.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
    
    def chng_cur1(self, event):
        wx.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        
    
    def on_iconbar_click(self, e):
        ev = e.GetLinkInfo().GetHref()
        
        if ev == "":
            pass

        elif ev == 'mark':
            self.move_item_marklist(None)
        elif ev == 'check_data':
            self.check_data(None)
        elif ev == 'listen':
            self.pronounce()
        elif ev == 'change':
            self.chck_grammar()
        
        elif ev == 'tmore':
            self.tmore = True
            self.load_item(self.cnt_item)
            
        elif ev == 'note':
            ff = clipboard.paste()
            self.Show_popup_note(ff)
            
        elif ev == 'trasl':
            
            self.get_info(None)
            #msg='Debe haver texto seleccionado'
            #title='Info'
            #dlg = wx.MessageDialog(self,message=msg,
                #caption=title,
                #style=wx.OK|wx.ICON_INFORMATION
               #)
            #ID = dlg.ShowModal() 
            #if ID == wx.ID_YES:
                #pass
                
        elif ev == 'hlight':
            self.edit_item(None)
            #self.Onhlight()

        elif ev == 'add':
            if self.auto_pronounce == False:
                self.auto_pronounce = True
            else:
                self.auto_pronounce = False
                
            #msg='Debe haver texto seleccionado'
            #title='Info'
            #dlg = wx.MessageDialog(self,message=msg,
                #caption=title,
                #style=wx.OK|wx.ICON_INFORMATION
              #)
            #ID = dlg.ShowModal()
            #if ID == wx.ID_YES:
                #pass
                
        elif ev == 'tag':
            
            print(self.html_field.SelectionToText())

            msg='Debe haver texto seleccionado'
            title='Info'
            dlg = wx.MessageDialog(self,message=msg,
                caption=title,
                style=wx.OK|wx.ICON_INFORMATION
              )
            ID = dlg.ShowModal() 
            if ID == wx.ID_YES:
                pass

    
    def delete_topic(self, event):
        msg='¿Está seguro de que desea borrar  "' + self.tpc + '" ?'
        title='Eliminar'
        dlg = wx.MessageDialog(self,message=msg,
            caption=title,
            style=wx.YES_NO|wx.ICON_QUESTION
          )
        ID = dlg.ShowModal() 
        if ID == wx.ID_YES:
            self.change_list_tpcs = True
            from tpc import delete
            c = delete.Topic(self.tpc)
        if ID == wx.ID_NO:
            pass

    def edit_note_image_close(self, event):
        txt = self.m_textCtrl4.GetValue()
        #self.label_img.SetLabel(txt)
        if self.stts_itemtype == 0:
            self.cur.execute('UPDATE Words SET note_img=? WHERE note_img=?',
            (txt,self.noteimg))
        elif self.stts_itemtype == 1:
            self.cur.execute('UPDATE Sentences SET note_img=? WHERE note_img=?',
            (txt,self.noteimg))
        self.db.commit()
        #self.label_img.Show()
        self.m_textCtrl4.Hide()
        self.tab_study.Layout()
        event.Skip()
        
    def edit_note_image_open(self, event):
        self.m_textCtrl4.SetValue(self.noteimg)
        self.m_textCtrl4.Show()
        #self.label_img.Hide()
        self.tab_study.Layout()
        event.Skip()
        
    def show_contens(self, event):
        wx.FileSystem.AddHandler(wx.ZipFSHandler())
        self.h = wx.html.HtmlHelpController()
        self.h.SetTempDir('/tmp/')
        self.h.AddBook('/usr/share/sniparse/ifs/help.zip', 1)
        self.h.DisplayContents()
    
    def player_pause(self):
        self.mediaPlayer.Pause()
        self.playbackSlider.SetValue(0)
        
    def player_play_stop(self, event):
        if self.b_play_enc.GetLabel() == "Stop":
            self.b_play_enc.SetLabel('Play')
            self.timer.Start(100)
            self.b_play_enc.SetBitmapLabel(wx.ArtProvider.GetBitmap(u"gtk-media-stop", wx.ART_MENU))
            self.mediaPlayer.Load(self.audio_attachmt)
            self.mediaPlayer.Play()
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.leng = self.mediaPlayer.Length()
            self.playbackSlider.SetRange(0, self.leng)
        elif self.b_play_enc.GetLabel() == "Play":
            self.b_play_enc.SetLabel('Stop')
            self.timer.Stop()
            self.b_play_enc.SetBitmapLabel(wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU))
            self.player_pause()
        event.Skip()
        
    def player_timer(self, event):
        offset = self.mediaPlayer.Tell()
        self.playbackSlider.SetValue(offset)
        if offset == 0:
            self.b_play_enc.SetLabel('Stop')
            self.b_play_enc.SetBitmapLabel(wx.ArtProvider.GetBitmap(u"gtk-media-play", wx.ART_MENU))

    def player_seek(self, event):
        offset = self.playbackSlider.GetValue()
        self.mediaPlayer.Seek(offset)
    
    def edit_topic_rename(self, parent):
        self.change_list_tpcs = True
        from tpc import rename
        rnm = rename.Topic(None)
        rnm.Show()
        
    def edit_topic_create(self, parent):
        self.change_list_tpcs = True
        from tpc import create
        new = create.Topic(None)
        new.Show()
        
    def edit_topic_import(self, event):
        self.change_list_tpcs = True
        wildcard = "*.idmnd"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            from tpc import _import
            path = path[0]
            new = _import.importingFile(path)
        dlg.Destroy()
        
    def show_dialog_about(self, event):
        from about import About
        l_w = About(self)
        
    def show_dialog_first(self, event):
        os.system("'/usr/share/sniparse/ifs/1u.py' & exit")
        
    def tool_searchupdates(self, event):
        from tools import brownser
        search = brownser()
        search.updts()
        
    def tool_feedback(self, event):
        from tools import brownser
        question = brownser()
        question.fdbk()
        
    def tool_donate(self, event):
        from tools import brownser
        donate = brownser()
        donate.mkdnt()
        
    def tool_website(self, event):
        from tools import brownser
        shared = brownser()
        shared.cmnty()
    
    def change_toolBarSize(self, event):
        self.Layout()
        z = self.GetSize()
        self.Qsixe_font2 = z[0]/80
        self.Qsixe_font = z[0]/40
        if self.Q_number == 3:
            self.QWHtml.SetStandardFonts(size=self.Qsixe_font2, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        else:
            self.QWHtml.SetStandardFonts(size=self.Qsixe_font, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        self.QWHtml.SetBackgroundImage(self.Qimg)
        self.m_auiToolBar1.SetMargins(wx.Size(z[0]/2-150+40,0))
        self.m_auiToolBar1.SetToolSeparation(25)
        self.m_auiToolBar1.Realize()
        self.Layout()
    
    def change_cursor_in_viewer(self, event):
        #dx,dy = self.html_field.ScreenToClient(wx.GetMousePosition())
        #z,x = self.GetSize()
        #cc = x/3
        #and dy < cc
        if self.stts_topic%2 != 1 and self.updt == True and self.stts_conj != True:
            if self.stts_acttools == False:
                self.stts_acttools = True
                self.load_item(self.cnt_item)
        else:
            pass
    
    def change_cursor_no_viewer(self, event):
        if self.stts_topic%2 != 1 and self.updt == True and self.stts_conj != True:
            if self.stts_acttools != False:
                self.stts_acttools = False
                self.load_item(self.cnt_item)
    
    def change_font_viewer(self, evt):
        id_ = evt.GetId()
        if id_ < 7:
            self.stts_fontstyle = id_
        else:
            if id_ == 7 and id_ < 12:
                self.stts_fontsize += 2
            elif id_ == 8:
                self.stts_fontsize -= 2
            elif id_ == 9:
                self.stts_fontsize = 18
        self.html_field.SetStandardFonts(size=self.stts_fontsize, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        self.QWHtml.SetStandardFonts(size=self.Qsixe_font, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
        
        if id_ == 10:
            self.gui()
        elif id_ == 12:
            self.ShowFullScreen(not self.IsFullScreen())

    def on_mousescroll(self,e):
        dx, dy = self.html_field.ScreenToClient(wx.GetMousePosition())
        z,x = self.GetSize()
        cc = x/3
        if dy < cc and self.stts_topic != 20:

            x = e.GetWheelRotation()
            if x > 0:
                self.stts_fontsize += 2
                if self.stts_fontsize > 96:
                    self.stts_fontsize = 96
            elif x < 0:
                self.stts_fontsize -= 2
                if self.stts_fontsize < 10:
                    self.stts_fontsize = 10
                
            self.html_field.SetStandardFonts(size=self.stts_fontsize, normal_face=self.lst_fontstyle[self.stts_fontstyle], fixed_face="")
            self.change_cursor_no_viewer(None)
            self.change_cursor_in_viewer(None)
        
        elif dy > cc:
            self.stts_acttools = True
            target = e.GetEventObject()
            p1 = target.GetScrollPos(wx.VERTICAL)
            e.Skip()
            self.Update()
            def updateScroll(p1,target,scroll_amt):
                p2 = target.GetScrollPos(wx.VERTICAL)
                if p1 == p2:#scroll did not effect target object so lets scroll our main panel
                    currScroll = self.html_field.GetViewStart()
                    print(currScroll)
                    newScroll = (currScroll[0],currScroll[1]- scroll_amt)
                    self.html_field.Scroll(*newScroll)
            wx.CallAfter(updateScroll,p1,target,e.GetWheelRotation()/120)
        

    def change_list(self, evt):
        from popuplists import Popuplists
        self.get_list_words()
        self.get_sentences_lst()
        self.get_images_lst()
        self.get_tags_lst()
        cnts = []
        if self.stts_topic%2 != 1:
            labels = [u"All", u"Words", u"Sentences", u"Marks", u"With Images", u"News", u"With Notes"]
            x = [len(self.lst_learning), self.cnt_words, self.cnt_sentences, len(self.lst_marks), self.cnt_Images, 1, 2]
        elif self.stts_topic%2 == 0:
            labels = [u"New items",  u"items Saved", u"Words", u"Sentences", u"Marks", u"With Images", u"With Notes"]
            x = [len(self.lst_learning), len(self.lst_learned), self.cnt_words, self.cnt_sentences, len(self.lst_marks)]
        for i in x:
            cnts.append(i)
        win = Popuplists(self, wx.SIMPLE_BORDER, self.Mode, self.stts_listmode, 
        self.lst_tags, cnts, self.stts_itemtype, labels)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0,0))
        sz =  btn.GetSize()
        win.Position(pos, (0-220, sz[1]-240))
        win.Popup()
    
    def Show_popup_note(self, ff):
        from popupnote import PopupNote
        word = self.html_field.SelectionToText()
        win = PopupNote(self.GetTopLevelParent(), wx.SIMPLE_BORDER)
        px = list(self.GetScreenPosition())
        win.Position((20, 20), (px[0]+200, px[1]+200))
        win.Show(True)

if __name__ == "__main__":
    app = wx.App(0)
    Topic(None).Show()
    #Thread(target = testok).start()
    app.MainLoop()
