#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ConfigParser
from BeautifulSoup import BeautifulSoup
import sqlite3
import feedparser
import threading
import time
import Queue
import pynotify
import os
import shutil
import re
import string
from time import strftime
import sys
import os.path
import tempfile
import random
import locale
import urllib2
import urllib
import lxml.html as lh
import ConfigParser
import goslate
gs = goslate.Goslate()
from var import tpc_dir, tpc_cdir, conf_dir, lng_dir, lng_cdir, lgtl, lgsl, tpc, lt, ls, tpc_db

reload(sys)
sys.setdefaultencoding("utf-8")

try:
    db = sqlite3.connect(tpc_db)
    cur = db.cursor()
    cur.execute("select Items from Items")
    newsList = cur.fetchall()
    newsList = [i[0] for i in newsList]
    cur.execute("select info1 from Topic")
    url = cur.fetchall()
    url = url[0]
    url = [x.encode('utf-8') for x in url[0].splitlines()]
    DT_t = tempfile.mkdtemp()
    os.chdir(DT_t)
    
except:
    print "Error parsing config file"


class check_download(object):
    
    def __init__(self):
        
        self.tpc_dir = tpc_dir
        pynotify.init('basic')
        osd = pynotify.Notification("Updating...", "Checking for new entries", "idiomind")
        osd.show()
        
        self.get_items()
        self.manag_deleting
       
    def get_items(self):
        
        number_of_url = 0
        number_of_entry = 0
        while number_of_url < 4:

            if url[number_of_url] != '':
                print '\nFetching data from  URL number '+str(number_of_url)
                try:
                    d = feedparser.parse(url[number_of_url])
                    items = d["items"]
                except:
                    print 'Error fetching data from URL number '+str(number_of_url)
                    
                #try:
                # ----------------------------------------------------------
                number_of_entry = 0
                while number_of_entry < 3:
                    #try:
                    print '\t- Get data of entry '+str(number_of_entry)
                    m_id = (''.join(random.choice(string.letters + string.digits) for i in range(12)))
                    e = d['entries'][number_of_entry]
                    trgt = e['title']
                    trgt = trgt.encode('ascii', 'ignore')
                    
                    cur.execute("select Items from Items")
                    newsList = cur.fetchall()
                    newsList = [i[0] for i in newsList]
                    check_trgt = trgt.split(" - ",1)[0]
                    
                    # if exist
                    # ----------------------------------------------------------
                    if check_trgt in newsList:
                        print check_trgt
                        print '\tItem already in the list!'
                        cur.execute("SELECT * FROM Sentences WHERE trgt=?", [(check_trgt)])
                        flds = cur.fetchall()
                        mdid = [i[12] for i in flds][0]
                        note1 = [i[15] for i in flds][0]
                        note2 = [i[16] for i in flds][0]
                        
                        if note1 == "":
                            smry1, smry2 = self.getsmy(e)
                            cur.execute('UPDATE Sentences SET note1=? WHERE note1=?',
                             (note1,smry1))
                            cur.execute('UPDATE Sentences SET note2=? WHERE note2=?',
                             (note2,smry2))
                            db.commit()
                    
                        if not os.path.exists(tpc_dir + '/' + mdid + '_l.mp3'):
                            self.getenc(e, mdid)
                        
                        if not os.path.exists(tpc_dir + '/' + mdid + '.jpg'):
                            self.getimg(e, mdid)
                            
                        pass
                    
                    # if not exist
                    # ----------------------------------------------------------
                    elif not trgt in newsList:
                        
                        link = e['link']
                        leading_item = items[number_of_entry]
                        trgt = re.sub("’", "'", trgt)
                        trgt = re.sub("#", "", trgt)
                        trgt = trgt.replace('\n', '')
                        smry1, smry2 = self.getsmy(e)
                        self.getenc(e, m_id)
                        self.getimg(e, m_id)

                        translation = gs.translate(trgt, ls)
                        translation = translation.encode(locale.getpreferredencoding())
                        srce = unicode(translation)
                        
                        try:
                            google_translate_url = 'https://translate.google.com/translate_tts'
                            opener = urllib2.build_opener()
                            opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
                            response = opener.open(google_translate_url+'?q='+trgt.replace(' ','%20')+'&tl=' + lt)
                            ofp = open(m_id + '.mp3','wb')
                            ofp.write(response.read())
                            ofp.close()
                            shutil.copyfile(m_id + '.mp3', tpc_dir + m_id + '.mp3')
                        except:
                            pass
                        
                        # If is a word
                        # ------------------------------------
                        if len(trgt.split(' ')) == 1:
                            grmr = ''
                            f1 = 0
                            f2 = 0
                            expl = ''
                            defn = ''
                            from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
                            hh = ['null', adjetives, adverbs, nouns, prepositions, pronouns, verbs]
                            index = 0
                            while index < len(hh):
                                chck = hh[index]
                                if any(str(trgt.lower()) in s for s in chck):
                                    f1 = index
                                index += 1
                            
                            if f1 != 0:
                                hh.pop(f1)
                                index = 0
                                while index < len(hh):
                                    chck = hh[index]
                                    if any(str(trgt.lower()) in s for s in chck):
                                        f2 = index
                                    index += 1
                            else:
                                f2 = 0
                            
                            img = ''
                            note = ''
                            cur.execute("insert into Words values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (trgt, grmr, srce, expl, defn, m_id, img, trgt, f1, f2, smry1, smry2, trgt, ''))

                        # Is is a sentence
                        # ------------------------------------
                        elif len(trgt.split(' ')) != 1:
                            
                            # process words of sentence
                            wrdt = ' '.join(word for word in trgt.split() if len(word)>2)
                            wrdt = re.sub(",;[!|&:?¿!.@#$]", "", wrdt)
                            wrdt = wrdt.strip().title()
                            wrdt = wrdt.replace('  ', ' ')
                            wrdt = wrdt.strip()
                            wrdt = wrdt.replace(' ', '\n')
                            
                            translation = gs.translate(wrdt, ls)
                            
                            if sys.version_info.major == 2:
                                translation = translation.encode(locale.getpreferredencoding())
                            wrds = unicode(translation)
                            
                            # process words of sentence again
                            swrds = wrds.strip()
                            twrds = wrdt.strip()
                            
                            # process grammar of sentence
                            gwrds = trgt.split()
                            from grmmr import adjetives, adverbs, nouns, prepositions, pronouns, verbs
                            lisv = ['adjetives', 'adverbs', 'nouns', 'prepositions', 'pronouns', 'verbs']
                            marks = [[],[],[],[],[],[]]
                            hl = [[],[],[],[],[],[]]
                            index = 0
                            while index < len(gwrds):
                                w = gwrds[index]
                                for idx in range(6):
                                    if any(str(w) in s for s in eval(lisv[idx])):
                                        marks[idx].append("<-" + str(idx+1) + "->" + w + "</-" + str(idx+1) + "->")
                                    else:
                                        marks[idx].append(w)
                                index += 1
                            for idx2 in range(6):
                                hl[idx2].append(' '.join(marks[idx2]))
                            img = ''
                            # save data in db
                            cur.execute("insert into Sentences values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (trgt, hl[0][0], hl[1][0], hl[2][0], hl[3][0], hl[4][0], hl[5][0], '', 0, srce, twrds, swrds, m_id, img, 20, smry1, smry2, trgt, link))
                        
                        # comun set
                        cur.execute("insert into Learning values (?)", (trgt,))
                        cur.execute("insert into Items values (?)", (trgt,))
                        db.commit()
                        
                        # show notify messagge
                        srce = srce + '\n' + '(' + tpc + ')'
                        pynotify.init('basic')
                        osd = pynotify.Notification(trgt, srce)
                        osd.show()
                                
                        #except:
                            #pass
                    else:
                        pass
                    number_of_entry += 1
            else:
                pass
                #except:
                    #print 'Error updating ' + url[n]
            number_of_url += 1

        shutil.rmtree(DT_t)
        
    
    def getsmy(self, e):
        
        print '\tGet summary...'
        try:
            smry = e['summary']
            smry = smry.encode('ascii', 'ignore')
            clean = re.compile(r'<[^>]+>')
            smry1 = clean.sub('', smry)
            smry1 = re.sub("’", "'", smry1)
            translation = gs.translate(smry1, ls)
            translation = translation.encode(locale.getpreferredencoding())
            smry2 = unicode(translation)
            smry1 = smry1.replace('. ', '. <br></br><br></br>')
            smry2 = smry2.replace('. ', '. <br></br><br></br>')
            print '\t   Ok'
        except:
            '\t   Could not get summary field'
            smry1 = ''
            smry2 = ''
        return smry1, smry2


    def getimg(self, e, mid):
        print '\tDownload image...'
        try:
            img = e['links'][0]['href']
        except:
            img = ""
        if not '.jpg' in img[-4:]:
            try:
                img = e['links'][1]['href']
            except:
                img = ""
            if not '.jpg' in img[-4:]:
                try:
                    img = e['links'][2]['href']
                except:
                    img = ""
                if not '.jpg' in img[-4:]:
                    try:
                        soup = BeautifulSoup(leading_item["description"])
                        img = soup.find("img")
                        img = img["src"]
                    except:
                        img = ""
                    if not '.jpg' in img[-4:]:
                        try:
                            img = soup.find("bpImage")
                            img = img["src"]
                        except:
                            img = ""
                        if not '.jpg' in img[-4:]:
                            pass
        if '.jpg' in img[-4:]:
            try:
                urllib.urlretrieve(img, mid + '.img.jpg')
                shutil.copyfile(mid + '.img.jpg', tpc_dir + '/' + mid + '.jpg')
                print '\t   Ok'
            except:
                pass
        else:
            print '\t   Could not get image file'
    
    
    def getenc(self, e, mid):
        print '\tDownload audio...'
        try:
            e_url = e['media_content'][0]['url']
        except:
            e_url = ""
        if not '.mp3' in e_url[-4:]:
            try:
                e_url = e['links'][0]['href']
            except:
                e_url = ""
            if not '.mp3' in e_url[-4:]:
                try:
                    e_url = e['links'][1]['href']
                except:
                    e_url = ""
                if not '.mp3' in e_url[-4:]:
                    try:
                        e_url = e['links'][2]['href']
                    except:
                        e_url = ""
                    if not '.mp3' in e_url[-4:]:
                            pass
        if '.mp3' in e_url[-4:]:
            try:
                urllib.urlretrieve(e_url, mid + '.audio.mp3')
                shutil.copyfile(mid + '.audio.mp3', tpc_dir  + '/' + mid + '_l.mp3')
                print '\t   Ok'
            except:
                pass
        else:
            print '\t   Could not get audio file'


    def manag_deleting(self):
        
        print '\nRemoving old entries...'
        cur.execute("select Items from Learning")
        lst = cur.fetchall()
        news_lst = [i[0] for i in lst][::-1]

        for x in range(15, len(news_lst)):
            print news_lst[x]
            cur.execute("DELETE FROM Items WHERE Items=?",(news_lst[x],))
            cur.execute("DELETE FROM Learning WHERE Items=?",(news_lst[x],))
            cur.execute("DELETE FROM Words WHERE trgt=?",(news_lst[x],))
            cur.execute("DELETE FROM Sentences WHERE trgt=?",(news_lst[x],))
        db.commit()
        print '\nOk'


if __name__ == "__main__":
    check_download()
