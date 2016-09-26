#!/usr/bin/python
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  6 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import sys, os
import ConfigParser
import sqlite3
import wx.animate
sys.path.insert(0, "/usr/share/sniparse")
from tools import ChopText

class Info ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 485,460 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer15 = wx.BoxSizer( wx.VERTICAL )
        
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
        
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        self.in_name = wx.StaticText( self.m_panel1, wx.ID_ANY, u"topic name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_name.Wrap( -1 )
        self.in_name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer16.Add( self.in_name, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 15 )
        
        
        
        
        sbSizer2.Add( bSizer16, 0, wx.EXPAND, 5 )
        
        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"General", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND, 5 )
        
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.t_category = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Category", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_category.Wrap( -1 )
        gSizer1.Add( self.t_category, 0, wx.ALL, 8 )
        
        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.in_category = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_category.Wrap( -1 )
        bSizer26.Add( self.in_category, 0, wx.ALL, 5 )
        
        self.b_editC = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-index", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
        bSizer26.Add( self.b_editC, 0, wx.RIGHT|wx.LEFT, 5 )
        
        
        gSizer1.Add( bSizer26, 1, wx.EXPAND, 5 )
        
        self.t_created = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Created", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_created.Wrap( -1 )
        gSizer1.Add( self.t_created, 0, wx.ALL, 8 )
        
        self.in_created = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_created.Wrap( -1 )
        gSizer1.Add( self.in_created, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8 )
        
        self.t_autor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Created by", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_autor.Wrap( -1 )
        gSizer1.Add( self.t_autor, 0, wx.ALL, 8 )
        
        self.in_autor = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_autor.Wrap( -1 )
        gSizer1.Add( self.in_autor, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8 )
        
        
        bSizer2.Add( gSizer1, 0, wx.EXPAND|wx.BOTTOM, 5 )
        
        self.ggg = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Content", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ggg.Wrap( -1 )
        self.ggg.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer2.Add( self.ggg, 0, wx.ALL, 5 )
        
        gSizer11 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.t_words = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Words", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_words.Wrap( -1 )
        gSizer11.Add( self.t_words, 0, wx.ALL, 8 )
        
        self.in_words = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_words.Wrap( -1 )
        gSizer11.Add( self.in_words, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8 )
        
        self.t_sentences = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Sentences", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_sentences.Wrap( -1 )
        gSizer11.Add( self.t_sentences, 0, wx.ALL, 8 )
        
        self.in_sentences = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_sentences.Wrap( -1 )
        gSizer11.Add( self.in_sentences, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8 )
        
        self.t_images = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Images", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_images.Wrap( -1 )
        gSizer11.Add( self.t_images, 0, wx.ALL, 8 )
        
        self.in_images = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_images.Wrap( -1 )
        gSizer11.Add( self.in_images, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8 )
        
        
        bSizer2.Add( gSizer11, 0, wx.EXPAND, 5 )
        
        
        bSizer17.Add( bSizer2, 1, wx.EXPAND|wx.ALL, 5 )
        
        bSizer21 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText22 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )
        self.m_staticText22.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer21.Add( self.m_staticText22, 0, wx.ALL|wx.EXPAND, 5 )
        
        gSizer12 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.t_stage = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Stage", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_stage.Wrap( -1 )
        gSizer12.Add( self.t_stage, 0, wx.ALL, 8 )
        
        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.in_stage = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_stage.Wrap( -1 )
        bSizer25.Add( self.in_stage, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.b_editS = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
        bSizer25.Add( self.b_editS, 0, wx.RIGHT|wx.LEFT, 5 )
        
        
        gSizer12.Add( bSizer25, 1, wx.EXPAND, 5 )
        
        self.t_learning = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Learning", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_learning.Wrap( -1 )
        gSizer12.Add( self.t_learning, 0, wx.ALL, 8 )
        
        self.in_learning = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_learning.Wrap( -1 )
        gSizer12.Add( self.in_learning, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.t_learned = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Learned", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_learned.Wrap( -1 )
        gSizer12.Add( self.t_learned, 0, wx.ALL, 8 )
        
        self.in_learned = wx.StaticText( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.in_learned.Wrap( -1 )
        gSizer12.Add( self.in_learned, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        bSizer21.Add( gSizer12, 0, wx.BOTTOM|wx.EXPAND, 5 )
        
        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        
        self.p_feeds = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer27 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer131 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText212 = wx.StaticText( self.p_feeds, wx.ID_ANY, u"Feeds", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText212.Wrap( -1 )
        self.m_staticText212.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer131.Add( self.m_staticText212, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_animCtrl1 = wx.animate.AnimationCtrl( self.p_feeds, wx.ID_ANY, wx.animate.NullAnimation, wx.DefaultPosition, wx.Size( 22,22 ), wx.animate.AC_DEFAULT_STYLE ) 
        bSizer131.Add( self.m_animCtrl1, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.b_feedupdate = wx.BitmapButton( self.p_feeds, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
        bSizer131.Add( self.b_feedupdate, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
        
        self.b_editU = wx.BitmapButton( self.p_feeds, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
        bSizer131.Add( self.b_editU, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer27.Add( bSizer131, 0, wx.EXPAND, 5 )
        
        bSizer13 = wx.BoxSizer( wx.VERTICAL )
        
        self.in_url0 = wx.StaticText( self.p_feeds, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.in_url0.Wrap( -1 )
        self.in_url0.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        self.in_url0.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
        self.in_url0.SetToolTipString( u"url1" )
        
        bSizer13.Add( self.in_url0, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 8 )
        
        self.in_url1 = wx.StaticText( self.p_feeds, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.in_url1.Wrap( -1 )
        self.in_url1.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer13.Add( self.in_url1, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 8 )
        
        self.in_url2 = wx.StaticText( self.p_feeds, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.in_url2.Wrap( -1 )
        self.in_url2.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer13.Add( self.in_url2, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 8 )
        
        self.in_url3 = wx.StaticText( self.p_feeds, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.in_url3.Wrap( -1 )
        self.in_url3.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer13.Add( self.in_url3, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 8 )
        
        
        bSizer27.Add( bSizer13, 0, wx.EXPAND, 5 )
        
        
        self.p_feeds.SetSizer( bSizer27 )
        self.p_feeds.Layout()
        bSizer27.Fit( self.p_feeds )
        bSizer12.Add( self.p_feeds, 0, wx.ALIGN_RIGHT|wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        self.p_activity = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.p_activity.Hide()
        
        bSizer272 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer1311 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2121 = wx.StaticText( self.p_activity, wx.ID_ANY, u"Activity", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2121.Wrap( -1 )
        self.m_staticText2121.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer1311.Add( self.m_staticText2121, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer272.Add( bSizer1311, 0, wx.EXPAND, 5 )
        
        
        self.p_activity.SetSizer( bSizer272 )
        self.p_activity.Layout()
        bSizer272.Fit( self.p_activity )
        bSizer12.Add( self.p_activity, 1, wx.ALIGN_RIGHT|wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer21.Add( bSizer12, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
        
        
        bSizer17.Add( bSizer21, 1, wx.EXPAND|wx.ALL, 5 )
        
        
        sbSizer2.Add( bSizer17, 1, wx.EXPAND, 5 )
        
        
        bSizer15.Add( sbSizer2, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        self.m_panel1.SetSizer( bSizer15 )
        self.m_panel1.Layout()
        bSizer15.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 0, wx.EXPAND, 15 )
        
        bSizer41 = wx.BoxSizer( wx.VERTICAL )
        
        self.b_close = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer41.Add( self.b_close, 0, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer41, 0, wx.ALIGN_RIGHT, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.b_feedupdate.Bind( wx.EVT_LEFT_UP, self.Update )
        self.b_editU.Bind( wx.EVT_LEFT_UP, self.editU )
        self.b_close.Bind( wx.EVT_LEFT_UP, self.close )
        

        #self.b_editU0.Bind( wx.EVT_LEFT_UP, self.editU0 )
        #self.b_editU1.Bind( wx.EVT_LEFT_UP, self.editU1 )
        #self.b_editU2.Bind( wx.EVT_LEFT_UP, self.editU2 )
        #self.b_editU3.Bind( wx.EVT_LEFT_UP, self.editU3 )
        #self.b_deleteU0.Bind( wx.EVT_LEFT_UP, self.deleteU0 )
        #self.b_deleteU1.Bind( wx.EVT_LEFT_UP, self.deleteU1 )
        #self.b_deleteU2.Bind( wx.EVT_LEFT_UP, self.deleteU2 )
        #self.b_deleteU3.Bind( wx.EVT_LEFT_UP, self.deleteU3 )
        

        self.load()
        try:
            self.in_url0.SetToolTipString(self.url[0])
            self.in_url1.SetToolTipString(self.url[1])
            self.in_url2.SetToolTipString(self.url[2])
            self.in_url3.SetToolTipString(self.url[3])
        except:
            pass
        
        
        
    def load(self):
        #try:
        HOME = os.getenv('HOME')
        self.cfgfile = HOME + '/.config/sniparse/prefs.cfg'
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(self.cfgfile)
        self.tpc = self.Config.get("Topic", "Name")
        lgtl = self.Config.get("Lang", "LGTL")
        lgsl = self.Config.get("Lang", "LGSL")
        self.DMLT = HOME + '/.sniparse/topics/' + lgtl + '/' + self.tpc + '/'
        self.DCMT = HOME + '/.config/sniparse/topics/' + lgtl + '/' + self.tpc + '/'
        tpc_db = self.DMLT + '/' + 'tpc'
        self.db = sqlite3.connect(tpc_db)
        self.cur = self.db.cursor()
        self.cur.execute("select Items from Learning")
        Learning = self.cur.fetchall()
        self.learning_lst = [i[0] for i in Learning]
        self.cur.execute("select Items from Learned")
        Learned = self.cur.fetchall()
        self.learned_lst = [i[0] for i in Learned]
        self.cur.execute("select trgt from Words")
        words = self.cur.fetchall()
        self.words_lst = [i[0] for i in words]
        self.cur.execute("select trgt from Sentences")
        sentences = self.cur.fetchall()
        self.sentences_lst = [i[0] for i in sentences]
        self.cur.execute("SELECT * FROM  Topic")
        self.flds = self.cur.fetchall()
        self.stts = [i[9] for i in self.flds][0]
        self.tpy = [i[3] for i in self.flds][0]
        self.url = [i[7] for i in self.flds][0]
        
        self.in_name.SetLabel(self.tpc)
        self.in_stage.SetLabel(str(self.stts))
        self.in_learning.SetLabel(str(len(self.learning_lst)))
        self.in_learned.SetLabel(str(len(self.learned_lst)))
        self.in_words.SetLabel(str(len(self.words_lst)))
        self.in_sentences.SetLabel(str(len(self.sentences_lst)))

        if self.stts%2 == 1:
            self.items = self.learning_lst
        elif self.stts%2 != 1:
            if self.stts != 20:
                self.p_feeds.Hide()
            else:
                self.p_feeds.Show()
                self.url = [x for x in self.url.splitlines()]
                i=0
                while i < len(self.url):
                    exec("self.in_url%s" % i + '.SetLabel(ChopText(self.url[i], 23))')
                    i += 1
        self.Fit()
        self.Layout()

    def editU( self, p):
        
        msg='Really want to do this?'
        title=''
        dlg = wx.MessageDialog(self,message=msg,
            caption=title,
            style=wx.YES_NO|wx.ICON_QUESTION,
           )
        ID = dlg.ShowModal() 
        if ID == wx.ID_YES:
            print 'yes'
         
        if ID == wx.ID_NO:
            pass
        
        #self.cur.execute('UPDATE Topic SET info1=? WHERE info1=?',
        #(stts,self.stts))
        #dl="DELETE FROM Learning"
        #self.cur.execute(dl)

    def Update( self, event ):
        os.system('python /usr/share/sniparse/updt_rss.py &')
        event.Skip()
        
    def close( self, event ):
        self.Close()
        event.Skip()
        
    
if __name__ == "__main__":
    app = wx.App(0)
    Info(None).Show()
    app.MainLoop()
