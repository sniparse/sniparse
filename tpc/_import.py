#!/usr/bin/python
# -*- coding: utf-8 -*- 

import ConfigParser
import sqlite3
import time
import Queue
import pynotify
import os
import shutil
import re
import string
from time import strftime
import sys
import wx
import os.path
import tempfile
import random
import locale
import lxml.html as lh
import subprocess
import json
from datetime import datetime, date
import getpass
sys.path.insert(0, "/usr/share/sniparse")
from var import tpc_dir, tpc_cdir, conf_dir, lng_dir, lng_cdir, lgtl, lgsl, tpc, lt, ls
from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
forms_list = ['null', adjetives, adverbs, nouns, prepositions, pronouns, verbs]

reload(sys)
sys.setdefaultencoding("utf-8")

class importingFile(object):
    def __init__(self, path):
        self.conf_dir = conf_dir
        self.lng_dir = lng_dir
        self.lng_cdir = lng_cdir
        self.tmp_dir = tempfile.mkdtemp()
        os.chdir(self.tmp_dir)
        self.tpc_lst = os.getenv('HOME') + '/.sniparse/topics/' + lgtl + '/.tpcs.json'
        if not os.path.exists(self.tpc_lst):

            with open(self.tpc_lst, 'wb') as index:
                json.dump({'own': [], 'itll': [], 'tpcs': []}, index, indent=4)
            
        with open(self.tpc_lst, 'rb') as index:
            indx = json.load(index)

        info = subprocess.check_output(['tail', '-1', path])
        info = info.replace('&', '\n')
        fields = re.split('\n',info)
        self.name = (fields[7].split('oname="'))[1].split('"')[0]
        self.lgsl = (fields[1].split('langs="'))[1].split('"')[0]
        self.lgtl = (fields[2].split('langt="'))[1].split('"')[0]
        
        self.create_topic(indx)
        self.add_data(path)
        self.download_fs()
        
    def create_topic(self, indx):
        self.name =  unicode(self.name)
        self.name = re.sub("[!|&:'@#$]", '', self.name)
        self.name = self.name.strip().capitalize()
        d = datetime.utcnow().strftime("%Y-%m-%d")
        user = getpass.getuser()
        n=1
        tpcs = indx['tpcs']
        if any(str(self.name) in s for s in tpcs):
            self.name = self.name + ' (' + str(n) + ')'
            n += 1
        os.chdir(self.lng_dir)
        os.makedirs(self.name)
        stts = open(self.lng_dir + '/' + self.name + '/review.cfg','w')
        print >> stts, '0.0|0|'+d

        own = indx['own']
        fd = indx['fd']
        itll = indx['itll']
        tpcs = indx['tpcs']
        own.append(self.name)
        tpcs.append(self.name)
        with open(self.tpc_lst, 'wb') as fp:
            json.dump({'own': own, 'fd': fd, 'itll': itll, 'tpcs': tpcs}, fp, indent=1)

        self.tpc_db = self.lng_dir + '/' + self.name + '/' + 'tpc'
        db = sqlite3.connect(self.tpc_db)
        cur = db.cursor()

        cur.execute("""CREATE TABLE Topic
                  (name TEXT, autor TEXT, 
                  category TEXT, type INTEGER, trgt TEXT, 
                  srce TEXT, note TEXT, info1 TEXT, 
                  info2 INTEGER, stts INTEGER)
               """)
        cur.execute('CREATE TABLE Items (Items TEXT)')
        cur.execute('CREATE TABLE Learning (Items TEXT)')
        cur.execute('CREATE TABLE Learned (Items TEXT)')

        cur.execute("""CREATE TABLE Sentences
                  (trgt TEXT, mrk1 TEXT, mrk2 TEXT, 
                  mrk3 TEXT, mrk4 TEXT, mrk5 TEXT, 
                  mrk6 TEXT, mrk7 TEXT, mrk INTEGER, 
                  srce TEXT, twrds TEXT, swrds TEXT, 
                  id TEXT, img TEXT, stts INTEGER, 
                  note1 TEXT, note2 TEXT, 
                  note_img TEXT, info1 TEXT)
               """)
        cur.execute("""CREATE TABLE Words
                  (trgt TEXT, grmr TEXT, srce TEXT, 
                  expl TEXT, defn TEXT, id TEXT, 
                  img TEXT, stts INTEGER, f1 INTEGER,
                   f2 INTEGER, note1 TEXT, note2 TEXT, note_img TEXT, info1 TEXT)
               """)
        cur.execute('CREATE TABLE Images (Items TEXT)')
        cur.execute('CREATE TABLE Marks (Items TEXT)')
        cur.execute('CREATE TABLE count (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q0bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q1bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q2bx4 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx0 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx1 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx2 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx3 (Items TEXT)')
        cur.execute('CREATE TABLE Q3bx4 (Items TEXT)')
        nt = ''
        try:
            cur.execute("INSERT INTO Topic (name, autor, type, trgt, srce, note, stts) VALUES (?, ?, ?, ?, ?, ?, ?)",
             (self.name, user, 1, self.lgtl, self.lgsl, '', 0.0))

        except sqlite3.IntegrityError:
            print('ERROR')
        db.commit()
        db.close()

        cfgfile = self.conf_dir + '/prefs.cfg'
        Config = ConfigParser.ConfigParser()
        Config.read(cfgfile)
        Config.set('Topic', 'name', self.name)
        Config.set('Topic', 'type', 'own')
        Config.set('Topic', 'last', 'mmm')
        cfgwrt = open(self.conf_dir + '/prefs.cfg','w')
        Config.write(cfgwrt)
        cfgwrt.close()
        
        time.sleep(0.5)
        pynotify.init("image")
        n = pynotify.Notification(self.name,
          "Is your topic now",
          "/usr/share/sniparse/images/cnn.png",
       )
        n.show()

        menu = open(self.conf_dir + '/.menu','w')
        print >>menu, self.name
        
        # import re
        # data = [line.strip() for line in open(path)]
        # item = data[1]
        # item = item.replace('},', '}\n')
        # fields = re.split('\n',item)
        # m_id = unicode((fields[11].split('id=['))[1].split(']')[0])
        #
        #['2:[type={2}', 'trgt={The possibility of a voyage to the moon is no longer remote.}', 'srce={La posibilidad de un viaje a la luna ya no es remota.}', 'exmp={}', 'defn={}', 'note={}', 'wrds={The_Las_Longer_M\xc3\xa1s_Moon_Luna_Possibility_Posibilidad_Remote_Remoto_The_Las_Voyage_Viaje_}', "grmr={<span color='#9C68BD'>The</span> possibility of a <span color='#62426A'>voyage</span> <span color='#9C68BD'>to</span> <span color='#9C68BD'>the</span> <span color='#62426A'>moon</span> <span color='#9C68BD'>is</span> no longer <span color='#62426A'>remote.</span>}", '].[tag={}', 'mark={}', 'link={}', '].id=[e24f9d73b7208246b166a07f220dbb4f]']

        
    def add_data(self, path):
        db = sqlite3.connect(self.tpc_db)
        cur = db.cursor()
        self.path = path
        data = [line.strip() for line in open(path)]
        cnt_lines = len(data)
          
        for item in data[:-1]:
            item = item.replace('},', '}\n')
            fields = re.split('\n',item)
            
            try:
                tipe = unicode((fields[0].split('type={'))[1].split('}')[0])
            except:
                tipe = "1"
            try:
                trgt = unicode((fields[1].split('trgt={'))[1].split('}')[0])
            except:
                trgt = "..."
            try:
                srce = unicode((fields[2].split('srce={'))[1].split('}')[0])
            except:
                srce = "..."
            try:
                expl = unicode((fields[3].split('exmp={'))[1].split('}')[0])
            except:
                expl = ""
            try:
                m_id = unicode((fields[11].split('id=['))[1].split(']')[0])
            except:
                try:
                    m_id = unicode((fields[12].split('id=['))[1].split(']')[0])
                except:
                    m_id = ""

            if trgt != '':
                self.tmp_dir = tempfile.mkdtemp()
                os.chdir(self.tmp_dir)
                tpc = self.name
                cur.execute("select Items from Items")
                index = cur.fetchall()
                index = [i[0] for i in index]

                if not trgt in index:
                    if trgt != "":
                        if tipe == str(1):
                            grmr = ''
                            f1 = 0
                            f2 = 0
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
                            note1 = ''
                            note2 = ''
                            defn = ''
                            cur.execute("insert into Words values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (trgt, grmr, srce, expl, defn, m_id, img, trgt, f1, f2, note1, note2, trgt, ''))
                            cur.execute("insert into Q0bx0 values (?)", (trgt,))
                            cur.execute("insert into Q1bx0 values (?)", (trgt,))
                            cur.execute("insert into Q2bx0 values (?)", (trgt,))

                        elif tipe == str(2):
                            wrdt = ' '.join(word for word in trgt.split() if len(word)>2)
                            wrdt = re.sub(",;[!|&:?¿!.@#$]", "", wrdt)
                            wrdt = wrdt.strip().title()
                            wrdt = wrdt.replace('  ', ' ')
                            wrdt = wrdt.strip()
                            wrdt = wrdt.replace(' ', '\n')
                            wrds = "uno dod"
                            swrds = wrds.strip()
                            twrds = wrdt.strip()

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

                            cur.execute("insert into Sentences values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (trgt, hl[0][0], hl[1][0], hl[2][0], hl[3][0], hl[4][0], hl[5][0], 
                             '', 0, srce, twrds, swrds, m_id, img, 0, '', '', trgt, ''))
                            cur.execute("insert into Q3bx0 values (?)", (trgt,))

                        cur.execute("insert into Learning values (?)", (trgt,))
                        cur.execute("insert into Items values (?)", (trgt,))
                        db.commit()
            else:
                pass
