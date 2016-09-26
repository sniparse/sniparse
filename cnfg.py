#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import ConfigParser
import os
import glib
sniparse = 'sniparse'
xdg_cnfg_dir = glib.get_user_config_dir()
cnfg_dir = os.path.join(xdg_cnfg_dir, sniparse)
autostart_dir = os.path.join(xdg_cnfg_dir, 'autostart')
autostart_file = os.path.join(autostart_dir, sniparse+'.desktop')
Sniparse = 'Sniparse'
version = '1.00'
comments = 'Languages Learning Tool'

if os.path.exists(autostart_file):
    autostart = True
else:
    autostart = False

class CnfigDlg ( wx.Frame ):
    
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Preferences", pos = wx.DefaultPosition, size = wx.Size( 520,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_toolBar1 = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,60 ), wx.TB_HORIZONTAL|wx.TB_TEXT ) 
        self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"General", wx.ArtProvider.GetBitmap( u"gtk-execute", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_RADIO, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_tool2 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"User Data", wx.ArtProvider.GetBitmap( wx.ART_FOLDER, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_RADIO, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_tool3 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Addons", wx.ArtProvider.GetBitmap( wx.ART_CDROM, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_RADIO, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.Realize() 
        
        bSizer1.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.p_1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.p_1.SetScrollRate( 5, 5 )
        bSizer14 = wx.BoxSizer( wx.VERTICAL )
        
        
        bSizer14.AddSpacer( ( 0, 0), 0, wx.TOP|wx.BOTTOM, 10 )
        
        bSizer7 = wx.BoxSizer( wx.VERTICAL )
        
        self.chk_sds = wx.CheckBox( self.p_1, wx.ID_ANY, u"Show dialog words selector", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chk_sds.SetValue(True) 
        bSizer7.Add( self.chk_sds, 0, wx.ALL, 5 )
        
        self.chk_sws = wx.CheckBox( self.p_1, wx.ID_ANY, u"Start with system", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.chk_sws, 0, wx.ALL, 5 )
        
        self.chk_ucg = wx.CheckBox( self.p_1, wx.ID_ANY, u"Algo mas", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.chk_ucg, 0, wx.ALL, 5 )
        
        
        bSizer14.Add( bSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.m_staticText7 = wx.StaticText( self.p_1, wx.ID_ANY, u"Edit audio with:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        gSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.CMD2 = wx.TextCtrl( self.p_1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.CMD2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.m_staticText8 = wx.StaticText( self.p_1, wx.ID_ANY, u"Voice syntetizer:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        gSizer2.Add( self.m_staticText8, 0, wx.ALL, 5 )
        
        self.CMD1 = wx.TextCtrl( self.p_1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.CMD1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.m_button6 = wx.Button( self.p_1, wx.ID_ANY, u"Audio imput", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_button6, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer14.Add( gSizer2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        gSizer1 = wx.GridSizer( 2, 2, 0, 0 )
        
        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2 = wx.StaticText( self.p_1, wx.ID_ANY, u"Language for Learning", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_staticText2.Wrap( -1 )
        bSizer16.Add( self.m_staticText2, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        gSizer1.Add( bSizer16, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.lng_trgtChoices = [ u"English", u"Spanish" ]
        self.lng_trgt = wx.Choice( self.p_1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.lng_trgtChoices, 0 )
        self.lng_trgt.SetSelection( 0 )
        gSizer1.Add( self.lng_trgt, 0, wx.ALL, 5 )
        
        bSizer161 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText21 = wx.StaticText( self.p_1, wx.ID_ANY, u"                You Language", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_staticText21.Wrap( -1 )
        bSizer161.Add( self.m_staticText21, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        gSizer1.Add( bSizer161, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        lng_trgt1Choices = [ u"English", u"Spanish" ]
        self.lng_trgt1 = wx.Choice( self.p_1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lng_trgt1Choices, 0 )
        self.lng_trgt1.SetSelection( 0 )
        gSizer1.Add( self.lng_trgt1, 0, wx.ALL, 5 )
        
        
        bSizer14.Add( gSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        self.p_1.SetSizer( bSizer14 )
        self.p_1.Layout()
        bSizer14.Fit( self.p_1 )
        bSizer2.Add( self.p_1, 1, wx.EXPAND, 5 )
        
        self.p_2 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.p_2.SetScrollRate( 5, 5 )
        
        bSizer19 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer20 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_checkBox5 = wx.CheckBox( self.p_2, wx.ID_ANY, u"Mantener una copia de seguridad", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer20.Add( self.m_checkBox5, 0, wx.ALL, 5 )
        
        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText3 = wx.StaticText( self.p_2, wx.ID_ANY, u"Folder Path", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        bSizer21.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_dirPicker1 = wx.DirPickerCtrl( self.p_2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer21.Add( self.m_dirPicker1, 0, wx.ALL, 5 )
        
        
        bSizer20.Add( bSizer21, 1, wx.EXPAND, 5 )
        
        
        bSizer19.Add( bSizer20, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 20 )
        
        bSizer23 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText4 = wx.StaticText( self.p_2, wx.ID_ANY, u"Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer23.Add( self.m_staticText4, 0, wx.RIGHT|wx.LEFT, 80 )
        
        
        bSizer19.Add( bSizer23, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_button5 = wx.Button( self.p_2, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.m_button5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        self.m_button4 = wx.Button( self.p_2, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.m_button4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        bSizer19.Add( bSizer22, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.p_2.SetSizer( bSizer19 )
        self.p_2.Layout()
        bSizer19.Fit( self.p_2 )
        bSizer2.Add( self.p_2, 1, wx.EXPAND, 5 )
        
        self.p_3 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.p_3.SetScrollRate( 5, 5 )
        
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        
        self.addonsChoices = []
        self.addons = wx.CheckListBox( self.p_3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.addonsChoices, 0 )
        bSizer6.Add( self.addons, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer3.Add( bSizer6, 1, wx.EXPAND, 5 )
        
        self.m_panel4 = wx.Panel( self.p_3, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_button1 = wx.Button( self.m_panel4, wx.ID_ANY, u"Config", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        
        self.m_panel4.SetSizer( bSizer5 )
        self.m_panel4.Layout()
        bSizer3.Add( self.m_panel4, 0, wx.TOP|wx.BOTTOM, 5 )
        
        
        self.p_3.SetSizer( bSizer3 )
        self.p_3.Layout()
        bSizer3.Fit( self.p_3 )
        bSizer2.Add( self.p_3, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
        
        bSizer17 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer18 = wx.BoxSizer( wx.VERTICAL )
        
        self.button_cls = wx.Button( self.m_panel5, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer18.Add( self.button_cls, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        self.m_panel5.SetSizer( bSizer18 )
        self.m_panel5.Layout()
        bSizer18.Fit( self.m_panel5 )
        bSizer17.Add( self.m_panel5, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer17, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_TOOL, self.A, id = self.m_tool1.GetId() )
        self.Bind( wx.EVT_TOOL, self.B, id = self.m_tool2.GetId() )
        self.Bind( wx.EVT_TOOL, self.C, id = self.m_tool3.GetId() )
        self.button_cls.Bind( wx.EVT_LEFT_UP, self.onClose )
        
        #self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.addons)
        #self.addons.SetSelection(0)
        self.load()
    

    
    # Virtual event handlers, overide them in your derived class
    def load(self):
        self.swith(1)
        
        self.cfgfile = os.getenv('HOME') + '/.config/sniparse/prefs.cfg'
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(self.cfgfile)
        
        LNGT = self.Config.get("Lang", "LGTL")
        LNGS = self.Config.get("Lang", "LGSL")
        LT = self.Config.get("Lang", "LGT")
        LS = self.Config.get("Lang", "LGS")
        ucg = self.Config.getboolean("Pref", "ucg")
        sds = self.Config.getboolean("Pref", "sds")
        sws = self.Config.getboolean("Pref", "sws")
        cmd1 = self.Config.get("Pref", "cmd1")
        cmd2 = self.Config.get("Pref", "cmd2")
        adds = self.Config.get("Addons", "keyword3")
        
        self.chk_sws.SetValue(autostart)
        self.chk_sds.SetValue(sds)
        self.chk_ucg.SetValue(ucg)
        self.CMD1.WriteText(cmd1)
        self.CMD2.WriteText(cmd2)
    
    def A( self, event ):
        self.swith(1)
        event.Skip()
    
    def B( self, event ):
        self.swith(2)
        event.Skip()
    
    def C( self, event ):
        self.swith(3)
        event.Skip()

    def swith(self, n):
        self.p_1.Hide()
        self.p_2.Hide()
        self.p_3.Hide()
        exec("self.p_"+str(n)+".Show()")
        self.Layout()
        
    def importf( self, event ):
        
        dlg = wx.FileDialog(self, "Import Data file", "", "",
                                   "*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.Path = dlg.GetPath()
            
        from UData import Importd
        Importd(self.Path)
            
        event.Skip()
    
    def exportf( self, event ):
        
        dlg = wx.FileDialog(self, "Save file", "", "",
                                   "*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.Path = dlg.GetPath()
            
        from UData import Exportd
        Exportd(self.Path)
        event.Skip()
    
    def grammar( self, event ):
        event.Skip()
    
    def word_selector( self, event ):
        event.Skip()
    
    def start_withSystem( self, event ):
        event.Skip()
    
    def audio_record( self, event ):
        event.Skip()
    
    def about_addon( self, event ):
        event.Skip()
    
    def config_addon( self, event ):
        event.Skip()
    
    
    
    def onClose( self, event ):
        self.Close()
         
        ucg = self.chk_ucg.GetValue()
        sds = self.chk_sds.GetValue()
        sws = self.chk_sws.GetValue()
        ch = self.lng_trgt.GetSelection()
        lngt = (self.lng_trgtChoices[ch])
        cmd1 = self.CMD1.GetValue()
        cmd2 = self.CMD2.GetValue()
        addons = self.addons.GetChecked()
        addons2 = self.addons.GetCheckedStrings()
        
        addons = [i for i in range(self.addons.GetCount()) if self.addons.IsChecked(i)] 

        self.Config.set('Pref', 'ucg', ucg)
        self.Config.set('Pref', 'sds', sds)
        self.Config.set('Pref', 'sws', sws)
        self.Config.set('Lang', 'LGTL', lngt)
        
        self.Config.set('Pref', 'cmd1', cmd1)
        self.Config.set('Pref', 'cmd2', cmd2)
        
        self.Config.set('Addons', 'keyword3', addons)

        cfgwrt = open(self.cfgfile,'w')
        self.Config.write(cfgwrt)
        
        if sws is True and os.path.exists(autostart_file) is False:
            self.autostart_create()
        elif sws is False and os.path.exists(autostart_file) is True:
            self.autostart_delete()
            
        cfgwrt.close()
        
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.addons.GetString(index)
        status = 'un'
        if self.addons.IsChecked(index):
            status = ''
        print ('%s is %schecked ' % (label, status))
        self.addons.SetSelection(index)
        
    def autostart_create(self):
        content = "\n"+"[Desktop Entry]\n"+"Type=Application\n"+"Exec="+sniparse+" --autostarted\n"+"X-GNOME-Autostart-enabled=true\n"+"Icon="+sniparse+"\n"+"Name="+Sniparse+"\n"+"Comment="+comments
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir, 0700)
        f = open(autostart_file, 'w')
        f.write(content)
        f.close()

    def autostart_delete(self):
        if os.path.exists(autostart_file):
            os.remove(autostart_file)
        

if __name__ == "__main__":
    app = wx.App(0)
    CnfigDlg(None).Show()
    #Thread(target = testok).start()
    app.MainLoop()
