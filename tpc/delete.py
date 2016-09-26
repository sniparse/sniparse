#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os, sys
import json
import sqlite3
import getpass
from configobj import ConfigObj
import ConfigParser
import shutil
import time
        
class Topic(object):
    
    def __init__(self, tpc):
        
        HOME = os.getenv('HOME')
        cfgfile = HOME + '/.config/sniparse/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)
        lgtl = Config.get("Lang", "lgtl")
        lgsl = Config.get("Lang", "lgsl")
        lt = Config.get("Lang", "lgt")
        ls = Config.get("Lang", "lgs")
        DML = HOME + '/.sniparse/topics/' + lgtl + '/'
        DCL = HOME + '/.config/sniparse/topics/' + lgtl + '/'
        DMLT = HOME + '/.sniparse/topics/' + lgtl + '/' + tpc + '/'
        DCMT = HOME + '/.config/sniparse/topics/' + lgtl + '/' + tpc + '/'
        tpc_db = HOME + '/.config/sniparse/topics/' + lgtl + '/' + tpc + '/' + 'tpc'

        tpc_lst = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/.tpcs.json'
        if not os.path.exists(tpc_lst):
            with open(tpc_lst, 'wb') as index:
                json.dump({'own': [], 'itll': [], 'tpcs': []}, index, indent=4)
        with open(tpc_lst, 'rb') as index:
            indx = json.load(index)


        # ojo aca tiene que cofig() leer el file primero antes de escribir
        
        cfgfile = HOME + '/.config/sniparse/prefs.cfg'
        Config.set('Topic', 'name', '')
        Config.set('Topic', 'type', 'own')
        Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(cfgfile,'w')
        Config.write(cfgwrt)
        cfgwrt.close()
        
        ## Rename database value
        #db = sqlite3.connect(tpc_db)
        #cur = db.cursor()
        #cur.execute('DELETE FROM Topic WHERE name=?',(tpc,))
        #db.commit()
        
        # Rename topic directories
        os.chdir(DML)
        shutil.rmtree(tpc)
        os.chdir(DCL)
        shutil.rmtree(tpc)
        
        # Rename in topics list
        own = indx['own']
        fd = indx['fd']
        itll = indx['itll']
        tpcs = indx['tpcs']
        
        if tpc in own:
            own.remove(tpc)
        if tpc in itll:
            itll.remove(tpc)
        tpcs.remove(tpc)

        with open(tpc_lst, 'wb') as fp:
            json.dump({'own': own, 'fd': fd, 'itll': itll, 'tpcs': tpcs}, fp, indent=1)

        ## Menu
        #menu = open(os.getenv('HOME') + '/.config/sniparse/.menu','w')
        os.system('$ > $HOME/.config/sniparse/.menu')
        #print >>menu, ''
        print 'Deleted'
