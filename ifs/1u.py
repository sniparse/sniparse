#!/usr/bin/python
# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import wx.html
from configobj import ConfigObj
import os
import shutil
import polib
import json
#po = polib.pofile('1u.po')

pags = ['<h3>Bienvenido</h3>Sniparse esta diseñado para ayudarte a aprender un lenguage extranjero, ya sea si eres principiante, o ya tienes un cierto manejo del idioma y deseas expandir tu vocabulario.<br />Veamos ahora unos conceptos para entender como funciona y asi conseguirás un mejor resultado', '<h3>Aprendisaje Activo </h3>El programa sugiere un aprendisaje activo. Esto es, que esta acondicionado para usuarios que utilizan documentos, páginas webs, ect. redactados en el lenguage que están aprendiendo', '<h3>Tomando Notas</h3>Cirscunstancialmente puedes encontrar frases o palabras que no conocías. dispones de un fácil acceso Puedes guardarlas facilmente, sin que sea necesario tener el programa abierto para ello.', '<h3>Aprendiendo en Contexto</h3>Las notas que se van agregando, que pueden ser oraciones o palabras, se podrán organizar en temáticas.Así será más fácil fijarse sus conceptos y además también, aprender como se usan en su ambiente nativo.', '<h3>Memoria a Largo plazo</h3>Se implement la técnica "Repetición Espaciada". Este Método mejorará el aprendisaje al distribuir gradualmente el tiempo entre los repasos en lugar de estudiar muchas veces en una sola sesión.' ,'<h3>FelizAprendisaje!</h3><br /><br />']

'''
pags = ['<h3>Bienvenido</h3>Sniparse esta diseñado para quienes están aprendiendo un lenguage extranjero, ya sea para principiantes, o los que ya tienen un cierto manejo del idioma y desean expandir su vocabulario.<br /><br />Veamos ahora unos conceptos para entender como funciona y asi lograr un mejor resultado', '<h4>Aprendisaje Activo </h4>El programa sugiere un aprendisaje activo. Esto es, que esta acondicionado para usuarios que utilizan documentos, páginas webs, ect. redactados en el lenguage que están aprendiendo', '<h4>Tomando Notas</h4>Cirscunstancialmente puedes encontrar frases o palabras que no conocías. dispones de un fácil acceso Puedes guardarlas facilmente, sin que sea necesario tener el programa abierto para ello.', '<h4>Aprendiendo en Contexto</h4>Las notas que se van agregando, que pueden ser oraciones o palabras, se podrán organizar en temáticas.Así será más fácil fijarse sus conceptos y además también, aprender como se usan en su ambiente nativo.', '<h4>Memoria a Largo plazo</h4>Se implement la técnica "Repetición Espaciada". Esto mejorará el aprendisaje distribuyendo gradualmente el tiempo entre los repasos en lugar de estudiar muchas veces en una sola sesión.' ,'<h5>FelizAprendisaje!</h5><br /><br />']
'''

path = '/usr/share/sniparse/images/'
imgs = [ path+'/f1.png', path+'/f1.png', path+'/f2.png', path+'/f3.png', path+'/f4.png']

class u1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Introduction", pos = wx.DefaultPosition, size = wx.Size( -1,160 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL )
        
        self.icon = wx.Icon(u"/usr/share/sniparse/images/cnn.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
        self.LNGT = ['English', 'Spanish', 'French']
        self.lt = ['en', 'es', 'fr']
        self.LNGS = ['English', 'Spanish', 'French']
        self.ls = ['en', 'es', 'fr']
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizerp1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizerp2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        self.m_panel2.Hide()
        
        self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.Size( 360,-1 ), wx.ALIGN_CENTRE )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        
        bSizer5.Add( self.m_staticText3, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 20 )
        
        
        bSizer5.AddSpacer( ( 0, 0), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        bSizer5_2 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer5_3 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Your Language :", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer5_3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
       
        self.lgtl = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), self.LNGT, 0 )
        self.lgtl.SetSelection( 0 )
        self.lgtl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer5_3.Add( self.lgtl, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        self.m_staticText11 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Language for Learning :", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_staticText11.Wrap( -1 )
        self.m_staticText11.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer5_3.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 10 )
        
        self.lgsl = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), self.LNGS, 0 )
        self.lgsl.SetSelection( 0 )
        self.lgsl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer5_3.Add( self.lgsl, 0, wx.ALL, 5 )
        
        
        bSizer5_2.Add( bSizer5_3, 1, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.TOP|wx.RIGHT|wx.LEFT, 10 )
        
        
        bSizer5.Add( bSizer5_2, 0, wx.ALL|wx.EXPAND, 5 )
        
        bSizer5_4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer13 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticline3 = wx.StaticLine( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer13.Add( self.m_staticline3, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        
        self.m_panel3.SetSizer( bSizer13 )
        self.m_panel3.Layout()
        bSizer13.Fit( self.m_panel3 )
        bSizer5_4.Add( self.m_panel3, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        
        bSizer5.Add( bSizer5_4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        bSizer5_5 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_button5 = wx.Button( self.m_panel2, wx.ID_ANY, u"Finish", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5_5.Add( self.m_button5, 0, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        self.b_cancel1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5_5.Add( self.b_cancel1, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        
        bSizer5.Add( bSizer5_5, 0, wx.ALIGN_RIGHT, 5 )
        
        
        self.m_panel2.SetSizer( bSizer5 )
        self.m_panel2.Layout()
        bSizer5.Fit( self.m_panel2 )
        bSizerp2.Add( self.m_panel2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        self.m_panel0 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel0.Show()
        
        bSizer0 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer0_1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_bitmap1 = wx.StaticBitmap( self.m_panel0, wx.ID_ANY, wx.Bitmap( u"/usr/share/sniparse/images/logo_mini.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 200,-1 ), 0 )

        bSizer0_1.Add( self.m_bitmap1, 0, wx.EXPAND, 5 )
        
        self.htmlWin = wx.html.HtmlWindow( self.m_panel0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 360,180 ), wx.html.HW_SCROLLBAR_AUTO )
        bSizer0_1.Add( self.htmlWin, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer0.Add( bSizer0_1, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        bSizer0_2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticline0 = wx.StaticLine( self.m_panel0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer0_2.Add( self.m_staticline0, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        
        bSizer0.Add( bSizer0_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        bSizer0_3 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.b_back = wx.Button( self.m_panel0, wx.ID_ANY, u"< Back", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer0_3.Add( self.b_back, 0, wx.TOP|wx.BOTTOM|wx.LEFT|wx.ALIGN_BOTTOM, 5 )
        
        self.b_next = wx.Button( self.m_panel0, wx.ID_ANY, u"Next >", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_next.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
        
        bSizer0_3.Add( self.b_next, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
        
        self.b_cancel = wx.Button( self.m_panel0, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer0_3.Add( self.b_cancel, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
        
        
        bSizer0.Add( bSizer0_3, 0, wx.ALIGN_RIGHT, 5 )
        
        
        self.m_panel0.SetSizer( bSizer0 )
        self.m_panel0.Layout()
        bSizer0.Fit( self.m_panel0 )
        bSizerp2.Add( self.m_panel0, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizerp1.Add( bSizerp2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizerp1 )
        self.Layout()
        bSizerp1.Fit( self )
        self.Fit()
        self.Centre( wx.BOTH )
        
        dw, dh = wx.DisplaySize()
        x = -1
        y = dh - 860
        self.SetPosition((x, y))
        
        # Connect Events
        self.m_button5.Bind( wx.EVT_LEFT_UP, self.apply )
        self.b_next.Bind( wx.EVT_LEFT_UP, self.f_next )
        self.b_back.Bind( wx.EVT_LEFT_UP, self.f_back )
        self.b_cancel.Bind( wx.EVT_LEFT_UP, self.f_cancel )
        self.b_cancel1.Bind( wx.EVT_LEFT_UP, self.f_cancel )
    
    
        self.htmlWin.SetPage(pags[0])
        #self.htmlWin.SetBackgroundColour(wx.NullColor)
        self.cpag = 0
        self.Refresh()
    
    
    def apply( self, event ):
        
        self.Destroy()
        HOME = os.getenv('HOME')
        
        # fetchinf values
        ch = self.lgtl.GetSelection()
        lgtl = (self.LNGT[ch])
        ch = self.lgsl.GetSelection()
        lgsl = (self.LNGS[ch])
        
        i = self.LNGT.index(lgtl)
        lgt = self.lt[i]
        i = self.LNGS.index(lgsl)
        lgs = self.ls[i]
                
        # evironment 
        if not os.path.exists(HOME + '/.sniparse'):
            os.makedirs(HOME + '/.sniparse/topics')
            os.makedirs(HOME + '/.sniparse/topics/saved/')
            os.makedirs(HOME + '/.config/sniparse')
            os.makedirs(HOME + '/.config/sniparse/topics/')
            os.makedirs(HOME + '/.config/sniparse/addons')
            os.makedirs(HOME + '/.config/sniparse/addons/dict/')
            os.makedirs(HOME + '/.config/sniparse/addons/stats/')
            os.makedirs(HOME + '/.config/sniparse/addons/practice/')
            os.makedirs(HOME + '/.config/sniparse/addons/news/')
            
            src = '/usr/share/sniparse/default/dicts'
            dest = HOME + '/.config/sniparse/addons/dict/'
            
            for f in os.listdir(src):
                ffn = os.path.join(src, f)
                if (os.path.isfile(ffn)):
                    shutil.copy(ffn, dest)
        
        # languages specific
        if not os.path.exists(HOME + '/.sniparse/topics/' + lgtl):
            os.makedirs(HOME + '/.sniparse/topics/' + lgtl)
            os.makedirs(HOME + '/.sniparse/topics/' + lgtl + '/.share/')
            os.makedirs(HOME + '/.config/sniparse/topics/' + lgtl)
        
        # writing values
        fc = HOME + '/.config/sniparse/prefs.cfg'
        config = ConfigObj()
        config['Topic'] = {}
        config['Topic']['Name'] = ''
        config['Topic']['Type'] = ''
        config['Topic']['Last'] = ''
        config['Lang'] = {}
        config['Lang']['LGT'] = lgt
        config['Lang']['LGS'] = lgs
        config['Lang']['LGTL'] = lgtl
        config['Lang']['LGSL'] = lgsl
        config['Pref'] = {}
        config['Pref']['lng'] = ''
        config['Pref']['ucg'] = False
        config['Pref']['sds'] = False
        config['Pref']['sws'] = True
        config['Pref']['cmd1'] = ''
        config['Pref']['cmd2'] = ''
        config['Addons'] = {}
        config['Addons']['keyword3'] = ''
        config['Addons']['keyword4'] = ''
        config['pos'] = {}
        config['pos']['x1'] = -1
        config['pos']['y1'] = -1
        config['pos']['x2'] = -1
        config['pos']['x2'] = -1
        config['pos']['w1'] = -1
        config['pos']['h1'] = -1
        config['misc'] = {}
        config['misc']['pgrm'] = 0
        config['misc']['modeList'] = 0
        config['misc']['lastItem'] = 0
        config['misc']['slide'] = False
        config['misc']['fontStyle'] = 0
        config['misc']['fontSize'] = 26
        config['misc']['showlider'] = True
        config['misc']['showpanel'] = True

        if not os.path.exists(fc):
            with open(fc, 'w') as configfile:
                config.write(configfile)
                config.write()
        # Index for topics
        tpc_lst = os.getenv('HOME') + '/.config/sniparse/topics/' + lgtl + '/.tpcs.json'
        if not os.path.exists(tpc_lst):
            with open(tpc_lst, 'wb') as index:
                json.dump({'own': [], 'fd': [], 'itll': [], 'tpcs': []}, index, indent=4)
        
    def f_next( self, event ):
        if self.cpag == 4:
            self.m_panel0.Hide()
            self.m_panel2.Show()
            self.Layout()
        else:
            self.cpag = self.cpag + 1
            self.img = imgs[self.cpag]
            self.htmlWin.SetPage(pags[self.cpag])
            self.img = wx.Image(imgs[self.cpag], wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            self.m_bitmap1.SetBitmap(self.img)
            self.htmlWin.SetBackgroundColour(wx.NullColor)
        event.Skip()

    def f_back( self, event ):
        self.cpag = self.cpag - 1
        self.img = imgs[self.cpag]
        self.htmlWin.SetPage(pags[self.cpag])
        self.img = wx.Image(imgs[self.cpag], wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.m_bitmap1.SetBitmap(self.img)
        self.htmlWin.SetBackgroundColour(wx.NullColor)
        event.Skip()
        
    def f_cancel( self, event ):
        self.Destroy()
        event.Skip()
    
if __name__ == "__main__":
    app = wx.App(0)
    u1(None).Show()
    app.MainLoop()
