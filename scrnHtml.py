#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import  wx.lib.wxpTag
import re
reload(sys)
sys.setdefaultencoding("utf-8")

colors = ["<font color='#5473B8'><b>", "<font color='#368F68'><b>", 
"<font color='#E08434'><b>", "<font color='#E08434'><b>", 
"<font color='#9C68BD'><b>", "<font color='#D14D8B'><b>"]

from wx.lib.embeddedimage import PyEmbeddedImage
from imgs import emoji
from barImages import *

mfs = wx.MemoryFSHandler()
wx.FileSystem_AddHandler(mfs)
imgs = PyEmbeddedImage(emoji)
mfs.AddFile("img.png", imgs.GetImage(), wx.BITMAP_TYPE_PNG)
lock = PyEmbeddedImage(lock)
mfs.AddFile("lock.png", lock.GetImage(), wx.BITMAP_TYPE_PNG)
unlock = PyEmbeddedImage(unlock)
mfs.AddFile("unlock.png", unlock.GetImage(), wx.BITMAP_TYPE_PNG)
checkFalse = PyEmbeddedImage(checkFalse)
mfs.AddFile("checkFalse.png", checkFalse.GetImage(), wx.BITMAP_TYPE_PNG)
checkTrue = PyEmbeddedImage(checkTrue)
mfs.AddFile("checkTrue.png", checkTrue.GetImage(), wx.BITMAP_TYPE_PNG)
edit = PyEmbeddedImage(markFalse)
mfs.AddFile("markFalse.png", edit.GetImage(), wx.BITMAP_TYPE_PNG)
info = PyEmbeddedImage(markTrue)
mfs.AddFile("markTrue.png", info.GetImage(), wx.BITMAP_TYPE_PNG)
listen = PyEmbeddedImage(listen)
mfs.AddFile("listen.png", listen.GetImage(), wx.BITMAP_TYPE_PNG)
hlight = PyEmbeddedImage(hlight)
mfs.AddFile("hlight.png", hlight.GetImage(), wx.BITMAP_TYPE_PNG)
change = PyEmbeddedImage(change)
mfs.AddFile("change.png", change.GetImage(), wx.BITMAP_TYPE_PNG)
trasl = PyEmbeddedImage(trasl)
mfs.AddFile("trasl.png", trasl.GetImage(), wx.BITMAP_TYPE_PNG)
add = PyEmbeddedImage(add)
mfs.AddFile("add.png", add.GetImage(), wx.BITMAP_TYPE_PNG)
tag = PyEmbeddedImage(tag)
mfs.AddFile("tag.png", tag.GetImage(), wx.BITMAP_TYPE_PNG)
note = PyEmbeddedImage(note)
mfs.AddFile("note.png", note.GetImage(), wx.BITMAP_TYPE_PNG)
tras = PyEmbeddedImage(tra)
mfs.AddFile("tras.png", tras.GetImage(), wx.BITMAP_TYPE_PNG)

def word(trgt, srce, expl, summary, note2, m, chng_list_stts, tpe, active_btns):
    
    if expl != '':
        expl = "&nbsp;" + expl + "&nbsp;"
    
    # check mark status
    if m is True:
        mark = 'markTrue'
    else:
        mark = 'markFalse'
    
    # check placed on list
    if chng_list_stts is True:
        if tpe == 0:
            check = 'checkTrue'
        elif tpe == 1:
            check = 'lock'
    elif chng_list_stts is False or chng_list_stts == None:
        if tpe == 0:
            check = 'checkFalse'
        elif tpe == 1:
            check = 'unlock'
            
    # check if have notes bgcolor="#F9F9F9"
    if summary != "":
        summary = """align="left" bgcolor="#F6F7F8"><font size="1" style=arial color="#424242">""" + summary + """</font>"""

    # check buttons on screen
    if active_btns == False:
        btns = """<table border="0" width="50%" align="center" cellpadding="5">
    <tr>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
    <tr>
   </table>"""
    elif active_btns == True:
        btns = """<table border="0" width="50%" align="center" cellpadding="5">
    <tr>
        <td align="center"><a href="note"><img src="memory:note.png"/></a></td>
        <td align="center"><a href="hlight"><img src="memory:hlight.png"/></a></td>
        <td align="center"><a href="change"><img src="memory:change.png"/></a></td>
        <td align="center"><a href="trasl"><img src="memory:trasl.png"/></a></td>
        <td align="center"><a href="add"><img src="memory:add.png"/></a></td>
        <td align="center"><a href="tag"><img src="memory:tag.png"/></a></td>
        <td align="center"><a href="listen"><img src="memory:listen.png"/></a></td>
    <tr>
   </table>"""
        
    card="""<body>
<table border="0" align="center" cellpadding="8">
<tr>
<td align="left"><a href="check_data"><img src="memory:""" + check + """.png"/></a></td>
<td align="left"><a href="mark"><img src="memory:""" + mark + """.png"/></a></td>
<td width="100%" align="left"></td>
<tr>
</table>
<table width="100%" border="0" align="center">
<tr>
<td width="5%" align="right"></td>
<td width="90%" align="center"><b><font size="8" color="#454545"><br>""" + trgt + """</font></b></td>
<td width="5%" align="right"></td>
</tr>
<tr>
<td width="5%" align="right"></td>
<td width="90%" align="center"><em><font size="1" color="#7D7D7D">""" + srce + """</font></em></td>
<td width="5%" align="right"></td>
</tr>
<tr>
<td align="right"></td>
<tr>
<tr>
<td width="5%" align="right"></td>
<td width="90%" align="center">""" + btns + """</td>
<td width="5%" align="right"></td>
</tr>
<tr>
<td align="right"><font size="1"></font></td>
<tr>
</table>
<table width="100%" border="0" align="center" cellpadding="15">
<tr>
<td width="10%" align="right"></td>
<td width="80%" """ + summary + """</td>
<td width="10%" align="right"></td>
</tr>
</table>
</body>"""
    return card

def sentence(trgt, srce, summary, m, chng_list_stts, gh, tpe, m_id, active_btns):
    audio = 'audio'
    
    # check notes
    if summary != "":
        summary = """align="left" bgcolor="#F6F7F8"><font size="1" style=arial color="#424242">""" + summary + """</font>"""
    else:
        summary = """align="left" bgcolor="#FFFFFF"><font size="1" style=arial color="#424242"></font>"""
        
    trgt = re.sub(r"<-"+str(gh)+"->", colors[gh], trgt)
    trgt = re.sub(r"</-"+str(gh)+"->", "</b></font>", trgt)
    
    # check marck status
    if m is True:
        mark = 'markTrue'
    else:
        mark = 'markFalse'
    # check list status
    if chng_list_stts is True:
        if tpe == 0:
            check = 'checkTrue'
        elif tpe == 1:
            check = 'lock'
    elif chng_list_stts is False or chng_list_stts == None:
        if tpe == 0:
            check = 'checkFalse'
        elif tpe == 1:
            check = 'unlock'
    

    # check button on screen
    if active_btns == False:
        btns = """<table border="0" width="50%" align="center" cellpadding="5">
    <tr>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
        <td align="center"><img src="memory:tras.png"/></td>
    <tr>
   </table>"""
    elif active_btns == True:
        btns = """<table border="0" width="50%" align="center" cellpadding="5">
    <tr>
        <td align="center"><a href="note"><img src="memory:note.png"/></a></td>
        <td align="center"><a href="hlight"><img src="memory:hlight.png"/></a></td>
        <td align="center"><a href="change"><img src="memory:change.png"/></a></td>
        <td align="center"><a href="trasl"><img src="memory:trasl.png"/></a></td>
        <td align="center"><a href="add"><img src="memory:add.png"/></a></td>
        <td align="center"><a href="tag"><img src="memory:tag.png"/></a></td>
        <td align="center"><a href="listen"><img src="memory:listen.png"/></a></td>
    <tr>
   </table>"""

    card="""<body>
<table border="0" align="center" cellpadding="8">
<tr>
<td align="left"><a href="check_data"><img src="memory:""" + check + """.png"/></a></td>
<td align="left"><a href="mark"><img src="memory:""" + mark + """.png"/></a></td>
<td width="100%" align="left"></td>
<tr>
</table>
<table width="100%" border="0" align="center">
<tr>
<td width="5%"></td>
<td width="90%" align="center"><font size="5" color="#454545"><b>""" + trgt + """</b></font></td>
<td width="5%"></td>
</tr>
<tr>
<td width="5%"></td>
<td width="90%" align="center"><em><font size="1" color="#7D7D7D">""" + srce + """</font></em></td>
<td width="5%"></td>
</tr>
<tr>
<td align="right"><font size="1"></font></td>
<tr>
<tr>
<td width="5%"></td>
<td width="90%" align="center">""" + btns + """</td>
<td width="5%"></td>
</tr>
<tr>
<td align="right"><font size="1"></font></td>
<tr>
</table>
<table width="100%" border="0" align="center" cellpadding="15">
<tr>
<td width="10%"></td>
<td width="80%" """ + summary + """</td>
<td width="10%"></td>
</tr>
</table>
</body>"""
    return card

def grammarm(selg, srce):
    card = """<br /><br /><font size="6" color="#454545">""" + selg + """</font><br /><br /><font size="3" color="#3C3C3C"><i>""" + srce + """</i></font>"""
    return card

def Conjugate(pro, verb, form):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="10" family="swiss" color="#3E3E3E"><br><br><b>""" + """<b>""" + pro + """</b>""" + verb + """<br></font></td><tr><td align="center"><em><font size="5" color="#AEACAC">""" + form + """</font></em></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td></td></tr></table>"""
    return card
    
def QStart(info):
    card = """<BODY bgcolor="#F1F1F1"></BODY><br><table width="100%" border="0" align="left"><td align="left"><font size="40" family="helvetica" color="#464646"></font></td><tr><td align="left"><font size="3" color="#797979"><br><br><br><br></font><font size="4" color="#3C3C3C">  """ + info + """</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card

def FlashcardsA(trgt, srce):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="6" color="#575555"><br><br><b>""" + trgt + """</b></font></td><tr><td align="center"><em><font size="4" color="#3C3C3C"><br><br></font></em></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
    
def FlashcardsAi(trgt, srce):
    card = """<br><br><table width="100%" border="0" align="center"><td align="center"><font size="10" family="helvetica" color="#FFFFFF"><br><br><b>""" + trgt + """</b></font></td><tr><td align="center"><em><font size="4" color="#FFFFFF"><br><br></font></em></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
    
def FlashcardsBi(trgt, srce):
    card = """<br><br><table width="100%" border="0" align="center"><td align="center"><font size="10" family="helvetica" color="#FFFFFF"><br><br><b>""" + trgt + """</b></font></td><tr><td align="center"><em><font size="4" color="#FFFFFF"><br><br>""" + srce + """</font></em></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card

def FlashcardsB(trgt, srce):
    card = """<br><table width="100%" height="50%" border="0" align="center"><td align="center"><font size="6" family="helvetica" color="#575555"><br><br><b>""" + trgt + """</b></font></td><tr><td align="center"></td></tr><tr><td align="center"><em><font size="3" color="#676F6D">""" + srce + """</font></em></td></tr></table>"""
    return card
    
def FlashcardsC(trgt, srce):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="10" color="#464646"><br><br><b></b></font></td><tr><td align="center"><font size="8" color="#6D6D6D"><b><br>""" + trgt + """</b></font></em></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
    
def FlashcardsD(trgt, srce):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="6" color="#575555"><br><br>""" + trgt + """</font><font size="4" color="#575555">    (<em>""" + srce + """</em>)</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
    
def FlashcardsE(trgt):
    card = """<table width="100%" border="0" align="center"><tr><td width="10%" align="left">&nbsp;</td><td width="80%" align="center"><font size="3" color="#404040"><b><br><br><br><br>""" + trgt + """</b></font></td><td width="10%" align="right">&nbsp;</td></tr></table>"""
    return card
    
def FlashcardsF(trgt, srce, prct):
    if prct > 80:
        exlt = 'Pass!'
    else:
        exlt = ''
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="6" color="#3C3C3C"><br><br>""" + trgt + """<br></font><font size="4" color="#3C3C3C">    (<em>""" + srce + """</em>)</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i>""" + str(prct) + """% </i><b><u> """ + exlt + """</b></u></font></td></tr></table>"""
    return card
    
def QEndA(src_r, src_w):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="5" color="#7BC765"><br><br>""" + str(src_r) + """<br></font><font size="4" color="#E76E6E">    """ + str(src_w) + """</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
    
def QEndB(src_r, src_w, c):
    if c is True:
        card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="5" color="#7BC765"><br><br><br>""" + str(src_r) + """<br><br></font><font size="4" color="#E76E6E">    """ + str(src_w) + """</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""   
    else:
        card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="5" color="#E76E6E"><br><br><br>""" + str(src_w) + """<br><br></font><font size="4" color="#7BC765">    """ + str(src_r) + """</font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>""" 
    return card
    
def Qnocnt(src_r):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="3" color="#7BC765"><br><br><br>No hay items necesarios para comenzar esta práctica""" + src_r + """<br><br></font><font size="4" color="#E76E6E"> </font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card

def Qokcnt(src_r):
    card = """<br><table width="100%" border="0" align="center"><td align="center"><font size="40" family="swiss" color="#464646"><br><b></b></font></td><tr><td align="center"><font size="3" color="#7BC765"><br><br><br>Has completado esta práctica""" + src_r + """<br><br></font><font size="4" color="#E76E6E"> </font></td></tr><tr><td align="center"><font size="2"><p></font></p></td></tr><tr><td align="center"><font size="3" color="#404040"><i></i></font></td></tr></table>"""
    return card
