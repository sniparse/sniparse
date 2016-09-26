#!/usr/bin/python
# -*- coding: utf-8 -*-

app_logo = '//usr/share/sniparse/images/logo_mini.png'
app_name = 'Idiomind'
app_version = '1.2'
app_comments = 'Vocabulary Learning Tool'
app_copyright = 'Copyright (C) 2015 Robin Palatnik'
app_website = 'http://idiomind.sourceforge.net'
import wx

class About(wx.Frame):
    
    def __init__(self, *args, **kwargs):

        app_license = (('This program is free software: you can redistribute it and/or modify\n'+
'it under the terms of the GNU General Public License as published by\n'+
'the Free Software Foundation, either version 3 of the License, or\n'+
'(at your option) any later version.\n'+
'\n'+
'This program is distributed in the hope that it will be useful,\n'+
'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'+
'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'+
'GNU General Public License for more details.\n'+
'\n'+
'You should have received a copy of the GNU General Public License\n'+
'along with this program.  If not, see <http://www.gnu.org/licenses/>.'))
        app_authors = ['Robin Palatnik<robinpalat@gmail.com>']
        app_documenters = ['Robin Palatnik<robinpalat@gmail.com>']
        description = "Vocabulary Learning Tool"

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('/usr/share/sniparse/images/llogo_mini.png', wx.BITMAP_TYPE_PNG))
        info.SetName(app_name)
        info.SetVersion(app_version)
        info.SetDescription(description)
        info.SetCopyright(app_copyright)
        info.SetWebSite(app_website)
        info.SetLicence(app_license)
        info.AddDeveloper('Robin Palatnik<robinpalat@gmail.com>')
        info.AddDocWriter('Robin Palatnik<robinpalat@gmail.com>')
        info.AddArtist('The Tango crew')
        info.AddTranslator('Jan Bodnar')
        wx.AboutBox(info)
