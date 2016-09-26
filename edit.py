#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import wx
import wx.xrc
from var import *
import re
import locale
import sys
import shutil
import sqlite3
import goslate
from wx.lib.embeddedimage import PyEmbeddedImage
reload(sys)
sys.setdefaultencoding("utf-8")

class eword ( wx.Frame ):
    
    def __init__( self, parent, trgt, tpc):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Edit Note", pos = wx.DefaultPosition, size = wx.Size( 460,525 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_FLOAT_ON_PARENT|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        
        # obteniendo datos
        #-----------------------------------------------------------

        tpc_db = tpc_dir + '/' + 'tpc'
        self.db = sqlite3.connect(tpc_db)
        self.cur = self.db.cursor()
        tpcs = indx['tpcs'][::-1]
        tpcs.remove(tpc)
        tpcs.insert(0,tpc)
        self.lst_tpcs = tpcs
        
        self.cur.execute("SELECT * FROM  Words WHERE trgt=?", [(trgt)])
        self.flds = self.cur.fetchall()
        
        self.id_media = [i[5] for i in self.flds][0]
       
        self.trgt = [i[0] for i in self.flds][0]
        self.srce = [i[2] for i in self.flds][0]
        self.expl = [i[3] for i in self.flds][0]
        self.defn = [i[4] for i in self.flds][0]
        self.note = [i[10] for i in self.flds][0]
        self.f1 = [i[8] for i in self.flds][0]
        self.f2 = [i[9] for i in self.flds][0]
        self.img = lng_dir + "/.share/images/" + self.trgt.lower() + '-0.jpg'
        

        frms1 = [ wx.EmptyString, u"Adjetive", u"Adverb", u"Noun", u"Preposition", u"Pronoun", u"Verb", u"Verbs-Noun" ]
        frms2 = [ wx.EmptyString, u"Adjetive", u"Adverb", u"Noun", u"Preposition", u"Pronoun", u"Verb", u"Verbs-Noun" ]
        
        hh1 = frms1[self.f1]
        hh2 = frms2[self.f2]
        
        if self.f1 != 0:
            frms1.remove(hh1)
            frms1.remove(wx.EmptyString)
            frms1.insert(0,hh1)
            self.frms1 = frms1
        else:
            self.frms1 = frms1

        if self.f2 != 0:
            frms2.remove(wx.EmptyString)
            frms2.remove(hh1)
            frms2.remove(hh2)
            frms2.insert(0,hh2)
            self.frms2 = frms2
        else:
            self.frms2 = frms2
        
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        
        
        bSizer61 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.w_image = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 120,100 ), 0 )
        bSizer10.Add( self.w_image, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10 )
        
        self.b_w_img = wx.Button( self.m_panel1, wx.ID_ANY, u"Add Image", wx.DefaultPosition, wx.Size( 60,20 ), 0 )
        self.b_w_img.SetFont( wx.Font( 6, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer10.Add( self.b_w_img, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 10 )

        
        bSizer81.Add( bSizer10, 0, wx.EXPAND, 5 )
        
        bSizer71 = wx.BoxSizer( wx.VERTICAL )
        
        self.edit_trgt = wx.StaticText( self.m_panel1, wx.ID_ANY, lgtl, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.edit_trgt.Wrap( -1 )
        self.edit_trgt.SetFont( wx.Font( 10, 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer71.Add( self.edit_trgt, 0, wx.TOP|wx.RIGHT|wx.LEFT, 10 )
        
        self.edit_srce = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_WORDWRAP )
        bSizer71.Add( self.edit_srce, 0, wx.ALL, 10 )
        
        
        bSizer81.Add( bSizer71, 1, wx.EXPAND, 5 )
        
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText9 = wx.StaticText( self.m_panel1, wx.ID_ANY, trgt + ' Is a:', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        bSizer16.Add( self.m_staticText9, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.type1Choices = self.frms1
        self.type1 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), self.type1Choices, 0 )
        self.type1.SetSelection( 0 )
        bSizer16.Add( self.type1, 0, wx.ALL, 5 )
        
        self.m_staticText12 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Y ademas es:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer16.Add( self.m_staticText12, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.type2Choices = self.frms2
        self.type2 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), self.type2Choices, 0 )
        self.type2.SetSelection( 0 )
        bSizer16.Add( self.type2, 0, wx.ALL, 5 )
        
        
        bSizer81.Add( bSizer16, 0, wx.RIGHT, 5 )
        
        
        bSizer61.Add( bSizer81, 0, wx.EXPAND, 5 )
        
        bSizer17 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText10 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Example", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        bSizer17.Add( self.m_staticText10, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.edit_expl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer17.Add( self.edit_expl, 1, wx.ALL|wx.EXPAND, 10 )
        
        self.m_staticText11 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Definition", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer17.Add( self.m_staticText11, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.edit_defn = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer17.Add( self.edit_defn, 1, wx.ALL|wx.EXPAND, 10 )
        
        
        bSizer61.Add( bSizer17, 1, wx.EXPAND, 5 )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText13 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Audio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        bSizer8.Add( self.m_staticText13, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.w_audio = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.mp3", wx.DefaultPosition, wx.Size( 300,-1 ), wx.FLP_DEFAULT_STYLE )
        bSizer8.Add( self.w_audio, 1, wx.ALL|wx.ALIGN_BOTTOM, 10 )
        
        
        bSizer61.Add( bSizer8, 0, wx.EXPAND, 5 )
        
        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText8 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Topic   ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_staticText8.Wrap( -1 )
        bSizer9.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.lst_tpcs = tpcs
        self.chng_tpc = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), self.lst_tpcs, 0 )
        self.chng_tpc.SetSelection( 0 )
        bSizer9.Add( self.chng_tpc, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        
        bSizer61.Add( bSizer9, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
        
        self.b_save = wx.Button( self.m_panel1, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.b_save, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.b_save.Enable( False )
        
        
        self.m_panel1.SetSizer( bSizer61 )
        self.m_panel1.Layout()
        bSizer61.Fit( self.m_panel1 )
        bSizer5.Add( self.m_panel1, 1, wx.EXPAND|wx.ALL, 15 )
        
        
        self.SetSizer( bSizer5 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        #-----------------------------------------------------------
        self.b_w_img.Bind( wx.EVT_LEFT_UP, self.image )
        self.b_save.Bind( wx.EVT_LEFT_UP, self.save )
        
        self.type1.Bind( wx.EVT_CHOICE, self.toButSv )
        self.type2.Bind( wx.EVT_CHOICE, self.toButSv )
        
        self.chng_tpc.Bind( wx.EVT_CHOICE, self.toButSv )
        self.w_audio.Bind( wx.EVT_FILEPICKER_CHANGED, self.toButSv )
        
        #buscando y estableciendo datos para mostrar
        #-----------------------------------------------------------

        #audio = lng_dirT + m_id + '.mp3'
        
        self.edit_trgt.SetLabel(self.trgt)
        self.edit_srce.WriteText(self.srce)
        self.edit_expl.WriteText(self.expl)
        self.edit_defn.WriteText(self.defn)
        
        if os.path.exists(self.img):
            
            img = wx.Image(self.img) 
            img.Rescale(120, 100) 
            img = wx.BitmapFromImage(img) 
            self.i = img
            self.w_image.SetBitmap(self.i)
            self.b_w_img.SetLabel('Remove Image')
        else:
            self.b_w_img.SetLabel('Add Image')
            
        self.edit_trgt.Bind( wx.EVT_TEXT, self.toButSv )
        self.edit_srce.Bind( wx.EVT_TEXT, self.toButSv )
        self.edit_expl.Bind( wx.EVT_TEXT, self.toButSv )
        self.edit_defn.Bind( wx.EVT_TEXT, self.toButSv )
        
    # Change o put image
    #-----------------------------------------------------------
    def toButSv(self, event):
        self.b_save.Enable( True )
        
    # set o put image
    #-----------------------------------------------------------
    def image(self, event):

        label = self.b_w_img.GetLabel()
        if label == 'Remove Image':
            if os.path.exists(self.img):
                os.remove(self.img)
            if os.path.exists('/tmp/.img.jpg'):
                os.remove('/tmp/.img.jpg')
            self.w_image.Hide()
            self.w_image.Layout()
            self.b_w_img.SetLabel('Add Image')
            
        else:
            import time
            os.system('cd /tmp; scrot -s --quality 80 .img.jpg')
            img = wx.Image('/tmp/.img.jpg')
            img.Rescale(100, 80)
            img = wx.BitmapFromImage(img) 
            self.w_image.SetBitmap(img)
            self.w_image.Show()
            self.w_image.Layout()
            self.b_w_img.SetLabel('Remove Image')

        self.b_save.Enable( True )

        

    # save the changes
    #-----------------------------------------------------------
    def save(self, event):
        

        # Get values
        m_id = [i[5] for i in self.flds][0] # media id for set audio or image

        srce_edt = self.edit_srce.GetValue()
        expl_edt = self.edit_expl.GetValue()
        defn_edt = self.edit_defn.GetValue()
        # note_edt = self.edt_w_n.GetValue()
        aud = self.w_audio.GetPath()
        ch = self.chng_tpc.GetSelection()
        tpc_edt = (self.lst_tpcs[ch])
        
        ################################################################
        ################################################################
        ################################################################
        frms = [wx.EmptyString, u"Adjetive", u"Adverb", u"Noun", u"Preposition", u"Pronoun", u"Verb", u"Verbs-Noun"]
        
        ch = self.type1.GetSelection()
        e_f1_label = (self.type1Choices[ch])
        e_f1 = frms.index(e_f1_label)
        
        ch = self.type2.GetSelection()
        e_f2_label = (self.type2Choices[ch])
        e_f2 = frms.index(e_f2_label)
        
        if self.f1 != e_f1:
            self.cur.execute('UPDATE Words SET f1=? WHERE f1=?',
            (e_f1,self.f1))
            self.db.commit()
            
        if self.f2 != e_f2:
            self.cur.execute('UPDATE Words SET f2=? WHERE f2=?',
            (e_f2,self.f2))
            self.db.commit()
            
        
        ################################################################
        ################################################################
        ################################################################
        
        
        
        # check changes in trgt
        #if trgt_edt != self.trgt:

            #self.cur.execute('UPDATE Words SET trgt=? WHERE trgt=?',
            #(trgt_edt,self.trgt))
            #self.cur.execute('UPDATE Items SET Items=? WHERE Items=?',
            #(trgt_edt,self.trgt))
            #self.cur.execute('UPDATE Learning SET Items=? WHERE Items=?',
            #(trgt_edt,self.trgt))
            #self.db.commit()
            
            #self.cur.execute("select Items from Learning")
            #Learning = self.cur.fetchall()
            #learning_lst = [i[0] for i in Learning]
            #Publisher().sendMessage("update itemss", learning_lst)
            #self.itmPaths = learning_lst
            #self.update()
            #self.Refresh()
            
        # check changes in srce
        if srce_edt != self.srce:
            
            self.cur.execute('UPDATE Words SET srce=? WHERE srce=?',
            (srce_edt,self.srce))
            self.db.commit()
            
        if expl_edt != self.expl:
            
            self.cur.execute('UPDATE Words SET expl=? WHERE expl=?',
            (expl_edt,self.expl))
            self.db.commit()
            
        if defn_edt != self.defn:
            
            self.cur.execute('UPDATE Words SET defn=? WHERE defn=?',
            (defn_edt,self.defn))
            self.db.commit()
            
        # check if set audio
        if aud:
            if os.path.exists(aud):
                shutil.copyfile(aud, lng_dir + '/' + tpc + '/' + self.id_media + '.mp3',)
        
        # check if set image
        if os.path.exists('/tmp/.img.jpg'):
                shutil.copyfile('/tmp/.img.jpg', lng_dir + '/' + tpc + '/' + self.id_media + '.jpg',)
            
            
            

        #if note_edt != note.srce:
            #self.cur.execute('UPDATE Words SET note=? WHERE note=?',
            #(note_edt,self.note))
            #self.db.commit()
            
        # check changes in list of topics
        if tpc_edt != tpc:
            
            trgt = [i[0] for i in self.flds][0]
            grmr = [i[1] for i in self.flds][0]
            srce = [i[2] for i in self.flds][0]
            expl = [i[3] for i in self.flds][0]
            defn = [i[4] for i in self.flds][0]
            m_id = [i[5] for i in self.flds][0]
            img = [i[6] for i in self.flds][0]
            f1 = [i[8] for i in self.flds][0]
            f2 = [i[9] for i in self.flds][0]
            note = [i[10] for i in self.flds][0]
            note_img = [i[11] for i in self.flds][0]
            stts = ''

            tpc_db_edt = DCL + tpc_edt + '/' + 'tpc.db'
            self.db_edt = sqlite3.connect(tpc_db_edt)
            self.cur_edt = self.db_edt.cursor()
            self.cur_edt.execute("insert into Words values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (trgt, grmr, srce, expl, defn, m_id, img, stts, f1, f2, note, note_img))

            self.cur_edt.execute("insert into Learning values (?)", (trgt,))
            self.cur_edt.execute("insert into Items values (?)", (trgt,))
            self.db_edt.commit()
            self.db_edt.close()

            self.cur.execute('DELETE FROM Items WHERE Items=?',(self.trgt,))
            self.cur.execute('DELETE FROM Learning WHERE Items=?',(self.trgt,))
            self.cur.execute('DELETE FROM Words WHERE trgt=?',(self.trgt,))
            self.db.commit()
           
        self.b_save.Enable( False )
        event.Skip()
        

class esntc ( wx.Frame ):
    
    def __init__( self, parent, trgt, tpc):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Edit Note", pos = wx.DefaultPosition, size = wx.Size( 710,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        tpc_db = tpc_dir + '/' + 'tpc'
        self.db = sqlite3.connect(tpc_db)
        self.cur = self.db.cursor()
        tpcs = indx['tpcs'][::-1]
        tpcs.remove(tpc)
        tpcs.insert(0,tpc)
        self.lst_tpcs = tpcs

        
        self.cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(trgt)])
        self.flds = self.cur.fetchall()
        self.id_media = [i[12] for i in self.flds][0]
        self.trgt = [i[0] for i in self.flds][0]
        self.srce = [i[9] for i in self.flds][0]
        self.twrds = [i[10] for i in self.flds][0]
        self.swrds = [i[11] for i in self.flds][0]
        self.img = [i[13] for i in self.flds][0]

        self.cur.execute("SELECT * FROM Topic")
        self.itpc = self.cur.fetchall()
        trgt = [i[4] for i in self.itpc][0]
        srce = [i[5] for i in self.itpc][0]

        self.SetSizeHintsSz( wx.Size( 710,360 ), wx.DefaultSize )

        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 340,-1 ) )
        
        bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
        
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel2, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )
        
        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer15 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, trgt, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        self.m_staticText6.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 50, 90, 92, False, wx.EmptyString ) )
        
        bSizer15.Add( self.m_staticText6, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.edit_trgt = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,100 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer15.Add( self.edit_trgt, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_staticText10 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.m_staticText10.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 50, 90, 92, False, wx.EmptyString ) )
        
        bSizer15.Add( self.m_staticText10, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.note1_edt = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,100 ), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer15.Add( self.note1_edt, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer10.Add( bSizer15, 1, wx.EXPAND, 5 )
        
        bSizer23 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText7 = wx.StaticText( self.m_panel2, wx.ID_ANY, srce, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer23.Add( self.m_staticText7, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.edit_srce = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,100 ), wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer23.Add( self.edit_srce, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.m_staticText9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 50, 90, 92, False, wx.EmptyString ) )
        
        bSizer23.Add( self.m_staticText9, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.note2_edt = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 160,100 ), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP )
        bSizer23.Add( self.note2_edt, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer10.Add( bSizer23, 1, wx.EXPAND, 5 )
        
        
        sbSizer2.Add( bSizer10, 1, wx.EXPAND, 5 )
        
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText12 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Words", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer16.Add( self.m_staticText12, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.words_list = wx.ListCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,100 ), wx.LC_ALIGN_LEFT|wx.LC_EDIT_LABELS|wx.LC_ICON|wx.LC_NO_HEADER|wx.LC_REPORT|wx.SUNKEN_BORDER )
        bSizer16.Add( self.words_list, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        sbSizer2.Add( bSizer16, 0, wx.EXPAND, 5 )
        
        
        bSizer14.Add( sbSizer2, 1, wx.EXPAND|wx.LEFT, 5 )
        
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel2, wx.ID_ANY, u"Image" ), wx.VERTICAL )
        
        bSizer24 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer24.SetMinSize( wx.Size( 150,120 ) ) 
        self.s_image = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 120,90 ), 0 )
        bSizer24.Add( self.s_image, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.b_s_img = wx.Button( self.m_panel2, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.Size( 80,22 ), 0 )
        self.b_s_img.SetFont( wx.Font( 7, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer24.Add( self.b_s_img, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 5 )
        
        
        sbSizer4.Add( bSizer24, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        bSizer9.Add( sbSizer4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        bSizer121 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText8 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Topic", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        bSizer121.Add( self.m_staticText8, 0, wx.RIGHT|wx.LEFT, 5 )
        
        chng_tpcChoices = self.lst_tpcs
        self.chng_tpc = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chng_tpcChoices, 0 )
        self.chng_tpc.SetSelection( 0 )
        bSizer121.Add( self.chng_tpc, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText11 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Audio mp3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer121.Add( self.m_staticText11, 0, wx.RIGHT|wx.LEFT, 5 )
        
        self.s_audio = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer121.Add( self.s_audio, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer9.Add( bSizer121, 0, wx.EXPAND|wx.ALL, 5 )
        
        
        bSizer14.Add( bSizer9, 0, wx.EXPAND, 5 )
        
        
        self.m_panel2.SetSizer( bSizer14 )
        self.m_panel2.Layout()
        bSizer14.Fit( self.m_panel2 )
        bSizer12.Add( self.m_panel2, 1, wx.EXPAND, 5 )
        
        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.b_delete = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer25.Add( self.b_delete, 0, wx.ALL, 5 )
        
        self.b_save = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer25.Add( self.b_save, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        
        bSizer12.Add( bSizer25, 0, wx.ALIGN_RIGHT, 5 )
        
        
        self.SetSizer( bSizer12 )
        self.Layout()
        
        self.Centre( wx.BOTH )


      
        # Connect Events
        #-----------------------------------------------------------
        self.b_s_img.Bind( wx.EVT_LEFT_UP, self.image )
        #self.b_w_img.Bind( wx.EVT_LEFT_UP, self.e_b_w_img )
        #self.b_save.Bind( wx.EVT_LEFT_UP, self.save )
        self.b_save.Bind( wx.EVT_LEFT_UP, self.save )

        self.s_audio.Bind( wx.EVT_FILEPICKER_CHANGED, self.toButSv )

        self.chng_tpc.Bind( wx.EVT_CHOICE, self.toButSv )
        
        self.edit_trgt.Bind( wx.EVT_TEXT, self.toButSv )
        self.edit_srce.Bind( wx.EVT_TEXT, self.toButSv )
        self.load(trgt)

    # buscando y estableciendo datos para mostrar
    #-----------------------------------------------------------
    def load(self, trgt):
        
        #self.words_list.InsertColumn(0, lgtl, width=45)
        #self.words_list.InsertColumn(1, lgsl, width=45)

        #twrds = [x.encode('utf-8') for x in self.twrds.splitlines()]
        #swrds = [x.encode('utf-8') for x in self.swrds.splitlines()]
        
        #index = 0
        #while index < len(twrds):
            #t = twrds[index].strip()
            #s = swrds[index].strip()
            #self.words_list.InsertStringItem(index, t)
            #self.words_list.SetStringItem(index, 1, s)
            #index += 1
        
        self.edit_trgt.WriteText(self.trgt)
        self.edit_srce.WriteText(self.srce)
        
        if os.path.exists(lng_dir + '/' + tpc + '/' + self.id_media + '.png'):
            img = wx.Image(lng_dir + '/' + tpc + '/' + self.id_media + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            img.Rescale(100, 80)
            img = wx.BitmapFromImage(img)
            self.s_image.SetBitmap(img)
            self.b_s_img.SetLabel('Remove Image')
        else:
            self.b_s_img.SetLabel('Add Image')
        
        self.b_save.Enable( False )
    
    
    # Change o put image
    #-----------------------------------------------------------
    def toButSv(self, event):
        self.b_save.Enable( True )
        
    
    # Change o put image
    #-----------------------------------------------------------
    def image(self, event):

        label = self.b_s_img.GetLabel()
        if label == 'Remove Image':
            if os.path.exists(lng_dir + '/' + tpc + '/' + self.id_media + '.jpg'):
                os.remove(lng_dir + '/' + tpc + '/' + self.id_media + '.jpg')
            if os.path.exists('/tmp/.img.jpg'):
                os.remove('/tmp/.img.jpg')
            self.s_image.Hide()
            self.s_image.Layout()
            self.b_s_img.SetLabel('Add Image')
            
        else:
            import time
            os.system('cd /tmp; scrot -s --quality 80 .img.jpg')
            img = wx.Image('/tmp/.img.jpg')
            img.Rescale(100, 80)
            img = wx.BitmapFromImage(img) 
            self.s_image.SetBitmap(img)
            self.s_image.Show()
            self.s_image.Layout()
            self.b_s_img.SetLabel('Remove Image')

        self.b_save.Enable( True )

    # save the changes
    #-----------------------------------------------------------
    def save(self, event):
        
        # Get general values
        trgt_edt = self.edit_trgt.GetValue()
        srce_edt = self.edit_srce.GetValue()
        ch = self.chng_tpc.GetSelection()
        aud = self.s_audio.GetPath()
        tpc_edt = (self.lst_tpcs[ch])
        gs = goslate.Goslate()
        
        
        # check changes in trgt
        if trgt_edt != self.trgt:

            from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
            import translator
            translator = translator.Translator(ls, lt)
            
            wrdt = ' '.join(word for word in trgt_edt.split() if len(word)>2)
            wrdt = re.sub(",;[!|&:?¿!.@#$]", "", wrdt)
            wrdt = wrdt.strip().title()
            wrdt = wrdt.replace('  ', ' ')
            wrdt = wrdt.strip()
            wrdt = wrdt.replace(' ', '\n')

            # Traslate words of sentence
            # translation = translator.translate(wrdt)
            translation = gs.translate(wrdt, ls)
            if sys.version_info.major == 2:
                translation = translation.encode(locale.getpreferredencoding())
            wrds = unicode(translation)
            
            # process words of sentence again
            self.cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(self.trgt)])
            self.flds = self.cur.fetchall()
            twrds_edt = wrds.strip()
            swrds_edt = wrdt.strip()
            twrds = [i[10] for i in self.flds][0]
            swrds = [i[11] for i in self.flds][0]
            
            # process grammar of sentence
            gwrds = trgt_edt.split()
            
            mrk1_edt = []
            mrk2_edt = []
            mrk3_edt = []
            mrk4_edt = []
            mrk5_edt = []
            mrk6_edt = []
            mrk7_edt = []
            mrk1 = [i[1] for i in self.flds][0]
            mrk2 = [i[2] for i in self.flds][0]
            mrk3 = [i[3] for i in self.flds][0]
            mrk4 = [i[4] for i in self.flds][0]
            mrk5 = [i[5] for i in self.flds][0]
            mrk6 = [i[6] for i in self.flds][0]
            mrk7 = [i[7] for i in self.flds][0]
            
            index = 0
            while index < len(gwrds):
                w = gwrds[index]
                
                if any(str(w) in s for s in adjetives):
                    mrk1_edt.append("<font color='#5473B8'>" + w + "</font>")
                else:
                    mrk1_edt.append(w)
                # ----------------
                if any(str(w) in s for s in adverbs):
                    mrk2_edt.append("<font color='#368F68'>" + w + "</font>")
                else:
                    mrk2_edt.append(w)
                # ----------------
                if any(str(w) in s for s in nouns):
                    mrk3_edt.append("<font color='#E08434'>" + w + "</font>")
                else:
                    mrk3_edt.append(w)
                    mrk7_edt.append(w)
                # ----------------
                if any(str(w) in s for s in prepositions):
                    mrk4_edt.append("<font color='#E08434'>" + w + "</font>")
                else:
                    mrk4_edt.append(w)
                # ----------------
                if any(str(w) in s for s in pronouns):
                    mrk5_edt.append("<font color='#9C68BD'>" + w + "</font>")
                else:
                    mrk5_edt.append(w)
                # ----------------
                if any(str(w) in s for s in verbs):
                    mrk6_edt.append("<font color='#D14D8B'>" + w + "</font>")
                else:
                    mrk6_edt.append(w)
                # ----------------
                index += 1

            mrk1_edt = ' '.join(mrk1_edt)
            mrk2_edt = ' '.join(mrk2_edt)
            mrk3_edt = ' '.join(mrk3_edt)
            mrk4_edt = ' '.join(mrk4_edt)
            mrk5_edt = ' '.join(mrk5_edt)
            mrk6_edt = ' '.join(mrk6_edt)
            mrk7_edt = ' '.join(mrk6_edt)
            mrk = 0
            stts = 0
            note = ''

            self.cur.execute('UPDATE Sentences SET trgt=? WHERE trgt=?',
            (trgt_edt,self.trgt))
            self.cur.execute('UPDATE Sentences SET mrk1=? WHERE mrk1=?',
            (mrk1_edt,mrk1))
            self.cur.execute('UPDATE Sentences SET mrk2=? WHERE mrk2=?',
            (mrk2_edt,mrk2))
            self.cur.execute('UPDATE Sentences SET mrk3=? WHERE mrk3=?',
            (mrk3_edt,mrk3))
            self.cur.execute('UPDATE Sentences SET mrk4=? WHERE mrk4=?',
            (mrk4_edt,mrk4))
            self.cur.execute('UPDATE Sentences SET mrk5=? WHERE mrk5=?',
            (mrk5_edt,mrk5))
            self.cur.execute('UPDATE Sentences SET mrk6=? WHERE mrk6=?',
            (mrk6_edt,mrk6))
            self.cur.execute('UPDATE Sentences SET mrk7=? WHERE mrk7=?',
            (mrk7_edt,mrk7))
            self.cur.execute('UPDATE Sentences SET twrds=? WHERE twrds=?',
            (twrds_edt,twrds))
            self.cur.execute('UPDATE Sentences SET swrds=? WHERE swrds=?',
            (swrds_edt,swrds))
            self.cur.execute('UPDATE Items SET Items=? WHERE Items=?',
            (trgt_edt,self.trgt))
            self.cur.execute('UPDATE Learning SET Items=? WHERE Items=?',
            (trgt_edt,self.trgt))
            self.db.commit()
            
        # check changes in srce
        if srce_edt != self.srce:
            
            self.cur.execute('UPDATE Sentences SET srce=? WHERE srce=?',
            (srce_edt,self.srce))
            self.db.commit()
        
        # check if set audio
        if aud:
            if os.path.exists(aud):
                shutil.copyfile(aud, lng_dir + '/' + tpc + '/' + self.id_media + '.mp3',)
        
        # check if set image
        if os.path.exists('/tmp/.img.jpg'):
            shutil.copyfile('/tmp/.img.jpg', lng_dir + '/' + tpc + '/' + self.id_media + '.jpg',)

            
        # check changes in list of topics
        if tpc_edt != tpc:
            
            trgt = [i[0] for i in self.flds][0]
            mrk1 = [i[1] for i in self.flds][0]
            mrk2 = [i[2] for i in self.flds][0]
            mrk3 = [i[3] for i in self.flds][0]
            mrk4 = [i[4] for i in self.flds][0]
            mrk5 = [i[5] for i in self.flds][0]
            mrk6 = [i[6] for i in self.flds][0]
            mrk7 = [i[7] for i in self.flds][0]
            mrk = [i[8] for i in self.flds][0]
            srce = [i[9] for i in self.flds][0]
            twrds = [i[10] for i in self.flds][0]
            swrds = [i[11] for i in self.flds][0]
            m_id = [i[12] for i in self.flds][0]
            img = [i[13] for i in self.flds][0]
            stts = [i[14] for i in self.flds][0]
            note1 = [i[15] for i in self.flds][0]
            note2 = [i[16] for i in self.flds][0]
            note_img = [i[17] for i in self.flds][0]
            
            tpc_db_edt = lng_dir + '/' + tpc_edt + '/' + 'tpc'
            self.db_edt = sqlite3.connect(tpc_db_edt)
            self.cur_edt = self.db_edt.cursor()
            self.cur_edt.execute("insert into Sentences values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (trgt, mrk1, mrk2, mrk3, mrk4, mrk5, mrk6, mrk7, 0, srce, twrds, swrds, m_id, img, 0, note1, note2, note_img, ''))

            self.cur_edt.execute("insert into Learning values (?)", (trgt,))
            self.cur_edt.execute("insert into Items values (?)", (trgt,))
            self.db_edt.commit()
            self.db_edt.close()
            
            if os.path.exists(tpc_dir + '/' + m_id + '.jpg'):
                shutil.copyfile(tpc_dir + '/' + m_id + '.jpg', lng_dir + '/' + tpc_edt + '/' + m_id + '.jpg',)
                    
            if os.path.exists(tpc_dir + '/' + m_id + '.mp3'):
                shutil.copyfile(tpc_dir + '/' + m_id + '.mp3', lng_dir + '/' + tpc_edt + '/' + m_id + '.mp3',)
            
            self.cur.execute('DELETE FROM Items WHERE Items=?',(self.trgt,))
            self.cur.execute('DELETE FROM Learning WHERE Items=?',(self.trgt,))
            self.cur.execute('DELETE FROM Sentences WHERE trgt=?',(self.trgt,))
            self.db.commit()
            
        self.b_save.Enable( False )
        event.Skip()
        
