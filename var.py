#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import json
import ConfigParser
from configobj import ConfigObj
e_dt = True
e_tpc = True

sdir = "/usr/share/sniparse/"
HOME = os.getenv('HOME')
cfgfile = HOME + '/.config/sniparse/prefs.cfg'
Config = ConfigParser.ConfigParser()
Config.read(cfgfile)
tpc = Config.get("Topic", "Name")
lgtl = Config.get("Lang", "lgtl")
lgsl = Config.get("Lang", "lgsl")
lt = Config.get("Lang", "lgt")
ls = Config.get("Lang", "lgs")
ucg = Config.getboolean("Pref", "ucg")
sds = Config.getboolean("Pref", "sds")
sws = Config.getboolean("Pref", "sws")

if not os.path.exists(cfgfile):
    import sys
    os.system("'/usr/share/sniparse/ifs/1u.py' &")
    sys.exit()

tpc_lst = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/.tpcs.json'
if not os.path.exists(tpc_lst):
    with open(tpc_lst, 'wb') as index:
        json.dump({'own': [], 'fd': [], 'itll': [], 'tpcs': []}, index, indent=4)
    
with open(tpc_lst, 'rb') as index:
    indx = json.load(index)

if tpc:
    tpc_dir = os.path.join(HOME, '.sniparse/topics', lgtl, tpc)
    tpc_cdir = os.path.join(HOME, '.config/sniparse/topics', lgtl, tpc)
else:
    e_tpc = False

conf_dir = os.path.join(HOME, '.config/sniparse')
lng_dir = os.path.join(HOME, '.sniparse/topics', lgtl)
lng_cdir = os.path.join(HOME, '.config/sniparse/topics', lgtl)

if tpc:
    tpc_db = tpc_dir + '/' + 'tpc'
else:
    e_db = False








