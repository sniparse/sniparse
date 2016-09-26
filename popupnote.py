#!/usr/bin/env python

import wx

class PopupNote(wx.PopupWindow):
    def __init__(self, parent, style):
        wx.PopupWindow.__init__(self, parent, style)
        

        panel = wx.Panel(self)
        self.panel = panel
        panel.SetBackgroundColour("#FFFADD")
        
        #import textwrap
        #text = textwrap.fill(text,20)
        
        
        st = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200,200), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_WORDWRAP)
    

        sz = st.GetBestSize()
        self.SetSize((200+10, 200+10))
        panel.SetSize((200+20, 200+20))

        #panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        #panel.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        #panel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        #panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        panel.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        panel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)    

    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.panel.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        if self.panel.HasCapture():
            self.panel.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        self.Destroy()
