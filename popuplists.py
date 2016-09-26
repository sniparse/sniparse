import wx

class Popuplists(wx.PopupTransientWindow):
    
    def __init__(self, parent, style, mode, stts_listmode, lst_tags, cnts,
        stts_itemtype, labels):
        wx.PopupTransientWindow.__init__(self, parent, style)
        Popuplists.mode = mode
        self.lst_tags = lst_tags
        self.stts_listmode = stts_listmode
        elements_ = labels+self.lst_tags
        n = 0
        self.rb_list = []
        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        self.panel.SetScrollRate(4, 4)
        self.panel.SetBackgroundColour("#F6F7F8")
        self.panel.SetSizeHintsSz(wx.Size(520,200), wx.DefaultSize)
        self.SetSizeHintsSz(wx.Size(520,205), wx.DefaultSize)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.gSizer1 = wx.GridSizer(0, 3, 0, 0)
        self.gSizer2 = wx.GridSizer(0, 3, 0, 0)
        bSizer2.Add(self.gSizer1, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        bSizer2.Add(self.gSizer2, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.panel.SetSizer(bSizer2)
        self.panel.Layout()
        bSizer2.Fit(self.panel)
        self.bSizer1.Add(self.panel, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5)

        for lbl in elements_:
            if n < 7:
                self.rb = wx.RadioButton(self.panel, n, lbl + '  (' + str(cnts[n]) + ')', wx.DefaultPosition, wx.DefaultSize, 0)
                self.gSizer1.Add(self.rb, 0, wx.ALL, 5)
            else:
                self.rb = wx.RadioButton(self.panel, n, '#' + lbl, wx.DefaultPosition, wx.DefaultSize, 0)
                self.gSizer2.Add(self.rb, 0, wx.ALL, 5)
            if n == stts_listmode:
                self.rb.SetValue(True)
 
            self.rb_list.append(self.rb)
            self.rb.Bind(wx.EVT_RADIOBUTTON, self.md)
            n = n+1

        self.SetSizer(self.bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        
    def md(self, evt):
        Popuplists.mode(evt.GetId())
        evt.Skip()
