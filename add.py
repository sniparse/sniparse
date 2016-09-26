#!/usr/bin/python
# -*- coding: utf-8 -*- 
import wx
import wx.xrc
import os
from var import *
import tempfile
import shutil
import sqlite3
import string
import random
import clipboard
import time
import re
import json
import sys
import locale
import urllib2
import wx.html
import os.path
import array
import goslate

from wx.lib.embeddedimage import PyEmbeddedImage
reload(sys)
sys.setdefaultencoding("utf-8")

own = indx['own'][::-1]
try:
    own.remove(tpc)
    own.insert(0,tpc)
except:
    print tpc

cfgfile = os.getenv('HOME') + '/.config/sniparse/prefs.cfg'
Config = ConfigParser.ConfigParser()
Config.read(cfgfile)
x1 = Config.get("pos", "x1")
y1 = Config.get("pos", "y1")


class Add ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "New note", pos = wx.DefaultPosition, size = wx.Size( 300,80 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        #self.SetSizeHintsSz(wx.Size(300,50), wx.DefaultSize)
        
        self.SetMaxSize( wx.Size( 300,120 ) )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_notebook1 = wx.Listbook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.BK_TOP|wx.SUNKEN_BORDER )
        self.m_notebook1.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        self.p_text = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_text.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer11 = wx.BoxSizer( wx.VERTICAL )
        
        self.text_trgt = wx.TextCtrl( self.p_text, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        self.text_trgt.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.text_trgt.SetMinSize( wx.Size( -1,30 ) )
        
        bSizer11.Add( self.text_trgt, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer3.Add( bSizer11, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.p_text.SetSizer( bSizer3 )
        self.p_text.Layout()
        bSizer3.Fit( self.p_text )
        self.m_notebook1.AddPage( self.p_text, u" English ", True )
        self.p_text1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.p_text1.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
        
        bSizer32 = wx.BoxSizer( wx.VERTICAL )
        
        self.text_srce = wx.TextCtrl( self.p_text1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer32.Add( self.text_srce, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.p_text1.SetSizer( bSizer32 )
        self.p_text1.Layout()
        bSizer32.Fit( self.p_text1 )
        self.m_notebook1.AddPage( self.p_text1, u" Spanish ", False )
        self.p_text2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.p_text2.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
        
        bSizer33 = wx.BoxSizer( wx.VERTICAL )
        
        self.text_expl = wx.TextCtrl( self.p_text2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer33.Add( self.text_expl, 1, wx.EXPAND, 5 )
        
        
        self.p_text2.SetSizer( bSizer33 )
        self.p_text2.Layout()
        bSizer33.Fit( self.p_text2 )
        self.m_notebook1.AddPage( self.p_text2, u" Example ", False )
        self.p_text3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.p_text3.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
        
        bSizer34 = wx.BoxSizer( wx.VERTICAL )
        
        self.text_defn = wx.TextCtrl( self.p_text3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer34.Add( self.text_defn, 1, wx.EXPAND, 5 )
        
        
        self.p_text3.SetSizer( bSizer34 )
        self.p_text3.Layout()
        bSizer34.Fit( self.p_text3 )
        self.m_notebook1.AddPage( self.p_text3, u" Definition ", False )
        self.p_text4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 180,50 ), 0 )
        #self.p_text4.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
        
        bSizer31 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2 = wx.StaticText( self.p_text4, wx.ID_ANY, u"Rec", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer71.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_gauge11 = wx.Gauge( self.p_text4, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,15 ), wx.GA_HORIZONTAL )
        self.m_gauge11.SetValue( 0 ) 
        bSizer71.Add( self.m_gauge11, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_bpButton211 = wx.BitmapButton( self.p_text4, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-media-record", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer71.Add( self.m_bpButton211, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer31.Add( bSizer71, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText1 = wx.StaticText( self.p_text4, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer7.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.m_filePicker1 = wx.FilePickerCtrl( self.p_text4, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( -1,20 ), wx.FLP_DEFAULT_STYLE )
        bSizer7.Add( self.m_filePicker1, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        self.m_filePicker1.SetSizeHintsSz( wx.Size( -1,30 ), wx.Size( -1,30 ) )
        
        
        bSizer31.Add( bSizer7, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.p_text4.SetSizer( bSizer31 )
        self.p_text4.Layout()
        self.m_notebook1.AddPage( self.p_text4, u" Audio ", False )
        
        bSizer1.Add( self.m_notebook1, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 0 )
        
        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.btn_image = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"/usr/share/sniparse/images/n.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
        bSizer15.Add( self.btn_image, 0, wx.ALIGN_BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        c_topics2Choices = own
        self.c_topics2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), c_topics2Choices, 0 )
        self.c_topics2.SetSelection( 0 )
        self.c_topics2.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer15.Add( self.c_topics2, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.b_save = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        bSizer15.Add( self.b_save, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer1.Add( bSizer15, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )
        
        self.Centre( wx.BOTH )
        
        #Connect Events

        # Connect Events
        self.btn_image.Bind( wx.EVT_KEY_UP, self.image )
        self.b_save.Bind( wx.EVT_LEFT_UP, self.get_Add )
        
        self.btn_image.Bind( wx.EVT_LEFT_UP, self.image )
        self.btn_image.Bind(wx.EVT_CONTEXT_MENU, self.onContext)

        
        self.text_trgt.SetBackgroundColour((255,255,255))

        #self.w_changes = wx.Timer(None)
        #self.w_changes.Bind(wx.EVT_TIMER, self.f_Refresh)
        #self.w_changes.Start(1000)
        
        self.c_topics2Choices = c_topics2Choices
    

        try:
            clip = clipboard.paste()
        except:
            pass
        if clip:
            text = self.text_trgt.SetValue(clip)
        else:
            text = ""

            

     # --------------------------------------------------------
     
    def get_Add( self, event ):

        event.Skip()
        
        trgt = self.text_trgt.GetValue()
        srce = self.text_srce.GetValue()
        expl = self.text_expl.GetValue()
        defn = self.text_defn.GetValue()
        note1 = ''
        note2 = ''
        
        ch = self.c_topics2.GetSelection()
        tpc_a = (self.c_topics2Choices[ch])
        self.tpc_dir = lng_dir + '/' + tpc_a
        
        self.Adding(trgt, srce, expl, defn, note1, note2, tpc_a)
        
     
    def Adding(self, trgt, srce, expl, defn, note1, note2, tpc_a):
        
        if trgt != '':

            DT_t = tempfile.mkdtemp()
            os.chdir(DT_t)
            tpc = tpc_a
            
            
            tpc_db = lng_dir + '/' + tpc + '/' + 'tpc'
            db = sqlite3.connect(tpc_db)
            cur = db.cursor()
            
            gs = goslate.Goslate()
            
            #import translator
            #translator = translator.Translator(ls, lt)
            

            m_id = (''.join(random.choice(string.letters + string.digits) for i in range(12)))
            trgt = str(trgt.encode('ascii', 'ignore'))
            trgt = re.sub("’", "'", trgt)
            srce = re.sub("’", "'", srce)
            trgt = trgt.replace('\n', '')
            srce = srce.replace('\n', '')
            
            translate_url = 'http://tts.baidu.com/text2audio'
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
            response = opener.open(translate_url+'?lan='+lt+'&ie=UTF-8&text='+trgt.replace(' ','%20'))
            
            ofp = open('speech.mp3','wb')
            ofp.write(response.read())
            ofp.close()

            # ------------------------------------
            if not srce:
                translation = gs.translate(trgt, ls)

                if sys.version_info.major == 2:
                    translation = translation.encode(locale.getpreferredencoding())
                srce = unicode(translation)

            else:
                srce = srce
            
            cur.execute("select Items from Items")
            index = cur.fetchall()
            index = [i[0] for i in index]

            if not trgt in index:
                
                # If is valid string
                if trgt != "":
                    
                    self.text_trgt.Clear()
                    self.text_srce.Clear()
                    os.system('xclip -i /dev/null')
                    #self.w_changes.Start()
                    self.text_trgt.SetBackgroundColour((255,255,255))
                    
                    # If is a word
                    # ------------------------------------
                    if len(trgt.split(' ')) == 1:
                    
                        if os.path.exists(DT_t + '/speech.mp3'):
                            shutil.copyfile('speech.mp3', self.tpc_dir + '/' + m_id + '.mp3')

                        if os.path.exists('/tmp/.img.jpg'):
                            shutil.copyfile('/tmp/.img.jpg', self.tpc_dir + '/' + m_id + '.jpg')
                            cur.execute("insert into Images values (?)", (trgt,))
                        grmr = ''
                        f1 = 0
                        f2 = 0
                        
                        ################################################################
                        ################################################################
                        ################################################################
                        
                        from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
                        forms_list = ['null', adjetives, adverbs, nouns, prepositions, pronouns, verbs]

                        index = 0
                        while index < len(forms_list):
                            chck = forms_list[index]

                            if any(str(trgt.lower()) in s for s in chck):
                                f1 = index
                            index += 1
                        
                        if f1 != 0:
                            forms_list.pop(f1)

                            index = 0
                            while index < len(forms_list):
                                chck = forms_list[index]
                                if any(str(trgt.lower()) in s for s in chck):
                                    f2 = index
                                index += 1
                        else:
                            f2 = 0
                        
                        img = ''
                        note = ''
                        cur.execute("insert into Words values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (trgt, grmr, srce, expl, defn, m_id, img, trgt, f1, f2, note1, note2, trgt, ''))
                        cur.execute("insert into Q0bx0 values (?)", (trgt,))
                        cur.execute("insert into Q1bx0 values (?)", (trgt,))
                        cur.execute("insert into Q2bx0 values (?)", (trgt,))
                        
                        
                         
                        ################################################################
                        ################################################################
                        ################################################################
                    
                    # Is is a sentence
                    # ------------------------------------
                    elif len(trgt.split(' ')) != 1:
                        
                        #if os.path.exists(DT_t + '/speech.mp3'):
                        shutil.copyfile('speech.mp3', self.tpc_dir + '/' + m_id + '.mp3')

                        if os.path.exists('/tmp/.img.jpg'):
                            shutil.copyfile('/tmp/.img.jpg', self.tpc_dir + '/' + m_id + '.jpg')

                        # process words of sentence
                        wrdt = ' '.join(word for word in trgt.split() if len(word)>2)
                        wrdt = re.sub(",;[!|&:?¿!.@#$]", "", wrdt)
                        wrdt = wrdt.strip().title()
                        wrdt = wrdt.replace('  ', ' ')
                        wrdt = wrdt.strip()
                        wrdt = wrdt.replace(' ', '\n')
      
                        # Traslate words of sentence
                        translation = gs.translate(wrdt, ls)
                        if sys.version_info.major == 2:
                            translation = translation.encode(locale.getpreferredencoding())
                        wrds = unicode(translation)
                        
                        # process words of sentence again
                        swrds = wrds.strip()
                        twrds = wrdt.strip()
                        #twrds = wrdt.replace('\n', '_')
                        #swrds = wrds.replace('\n', '_')
                        
                        # process grammar of sentence
                        gwrds = trgt.split()
                        from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
                        lisv = ['adjetives', 'adverbs', 'nouns', 'prepositions', 'pronouns', 'verbs']
                        marks = [[],[],[],[],[],[]]
                        index = 0
                        while index < len(gwrds):
                            w = gwrds[index]
                            for idx in range(6):
                                if any(str(w) in s for s in eval(lisv[idx])):
                                    marks[idx].append("<-" + str(idx+1) + "->" + w + "</-" + str(idx+1) + "->")
                                else:
                                    marks[idx].append(w)
                            index += 1
                        hl = [[],[],[],[],[],[]]
                        for idx2 in range(6):
                            hl[idx2].append(' '.join(marks[idx2]))
                        img = ''
                        # save data in db
                        cur.execute("insert into Sentences values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (trgt, hl[0][0], hl[1][0], hl[2][0], hl[3][0], hl[4][0], hl[5][0], '', 0, srce, twrds, swrds, m_id, img, 0, '', '', trgt, ''))
                        cur.execute("insert into Q3bx0 values (?)", (trgt,))

                    # comun set
                    cur.execute("insert into Learning values (?)", (trgt,))
                    cur.execute("insert into Items values (?)", (trgt,))
                    db.commit()
                    
                    srce = srce + '\n' + '(' + tpc + ')'
                    
                    import pynotify
                    # image check y notifing
                    if os.path.exists('/tmp/.img.jpg'):
                        
                        img = '/tmp/.img.jpg'
                        # show notify messagge with image
                        pynotify.init('image')
                        n = pynotify.Notification(trgt, srce, img)
                        n.show()
                    else:
                        # show notify messagge
                        pynotify.init('basic')
                        n = pynotify.Notification(trgt, srce)
                        n.show()
            
            #os.remove('/tmp/.img.jpg')
            image = wx.Image('/usr/share/sniparse/images/n.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            self.btn_image.SetBitmapLabel(image)
            self.btn_image.Refresh()
            
            if os.path.exists('/tmp/.img.jpg'):
                os.remove('/tmp/.img.jpg')
                
            
        else:
            pass
        
    
    # --------------------------------------------------------
    def onContext(self, event):
 
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.itemTwoId = wx.NewId()
            self.itemThreeId = wx.NewId()
            self.Bind(wx.EVT_MENU, self.imgviw, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.imgsrch, id=self.itemTwoId)
            self.Bind(wx.EVT_MENU, self.imgdel, id=self.itemThreeId)
 
        menu = wx.Menu()
        itemOne = menu.Append(self.popupID1, "Image Viewer")
        itemTwo = menu.Append(self.itemTwoId, "Search Image On Internet")
        itemThree = menu.Append(self.itemThreeId, "Delete")
 
        self.PopupMenu(menu)
        menu.Destroy()
 
    def imgviw(self, event):
        if os.path.exists('/tmp/.img.jpg'):
            import cimg
            im = cimg.cmain('/tmp/.img.jpg')
            from tools import Imv
            imv = Imv(self)
            imv.ShowModal()
            imv.Destroy()
        else:
            event.Skip()
        
    def imgsrch(self, event):
        
        trgt = self.text_trgt.GetValue()
        if not trgt:
            msg = wx.MessageBox('Must write words en text box', 
                                   'Info', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        else:
            import webbrowser
            webbrowser.open('https://www.google.com/search?q=' + trgt + '&tbm=isch')
 
    def imgdel(self, event):
        
        image = wx.Image('/usr/share/sniparse/images/n.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.btn_image.SetBitmapLabel(image)
        self.btn_image.Refresh()
        if os.path.exists('/tmp/.img.jpg'):
                os.remove('/tmp/.img.jpg')
        
    def OnClose(self, event):

        tpl = list(self.GetScreenPosition())
        Config.set('pos', 'x1', tpl[0])
        Config.set('pos', 'y1', tpl[1])
        cfgwrt = open(os.getenv('HOME') + '/.config/sniparse/prefs.cfg','w')
        Config.write(cfgwrt)
        cfgwrt.close()
       
        if os.path.exists('/tmp/.img.jpg'):
                os.remove('/tmp/.img.jpg')
            
        self.Destroy()
        event.Skip()


    # --------------------------------------------------------
    def image( self, event ):
        
        if os.path.exists('/tmp/.img.jpg'):
            from tools import Imv
            imv = Imv(self)
            imv.ShowModal()
            imv.Destroy()
        else:
            os.system('cd /tmp; scrot -s --quality 80 .img.jpg')
            time.sleep(0.1)
            img = wx.Image('/tmp/.img.jpg') 
            img.Rescale(22, 22)
            img = wx.BitmapFromImage(img) 
            self.btn_image.SetBitmapLabel(img)
            self.btn_image.Refresh()
    
        
    #----------------------------------------------------------------------
    def mxlen1(self, event):
        
        txt = self.text_trgt.GetValue()
        self.text_trgtM.WriteText(txt)
        self.text_trgtM.SetFocus()
        self.text_trgt = self.text_trgtM
        self.text_srce = self.text_srceM
        
    def mxlen2(self, event):
        
        msg = wx.MessageBox('Must write less characters', 
                                   'Info', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        
        
        
    #def paste( self, event ):
        #self.text_trgt.WriteText(clipboard.paste())
        #os.system('xclip -i /dev/null')
        #self.m_toolBar1.EnableTool( 0, False )
        
        
    def audio( self, event ):
        self.text_trgt.WriteText(clipboard.paste())

if __name__ == "__main__":
    app = wx.App(0)
    Add(None).Show()
    app.MainLoop()
    
    
    
    
    
    
    

