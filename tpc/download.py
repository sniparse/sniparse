#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ConfigParser
from os.path import abspath, realpath, dirname, join
from sys import stderr
import sqlite3
import time
import Queue
import pynotify
import os
import shutil
import re
import string
import sys
import tempfile
import tarfile
import locale
import urllib2 as request
sys.path.insert(0, "/usr/share/sniparse")
from var import tpc_db, tpc_dir, tpc_cdir, conf_dir, lng_dir, lng_cdir, lgtl, lgsl, tpc, lt, ls
reload(sys)
sys.setdefaultencoding("utf-8")


class downloadFiles(object):
    def __init__(self):
        db = sqlite3.connect(tpc_db)
        cur = db.cursor()
        langt = "English"
        lgtl = langt.lower()+"/"
        ilink = "p92"+"."
        md5id = "951a9ec5403c966dab5db1616f461575"
        oname = unicode("The Benefits of Breakfast")
        url = 'http://idiomind.sourceforge.net/doc/SITE_TMP'
        cont = True
        try:
            sitetmp = request.urlopen(url)
            sitetmp = sitetmp.read().decode('utf-8').split()
            url = (sitetmp[0].split('DOWNLOADS="'))[1].split('"')[0]
        except:
            cont = False
            print "Error on get url for download"
        
        tmp_dir = tempfile.mkdtemp()
        tar_url = url + '/c/' + lgtl + ilink + md5id + ".tar.gz"
        print tar_url
        src_dir_atth = os.path.join(tmp_dir, oname, 'files')
        dst_dir_atth = os.path.join(tpc_dir, 'files')
        src_dir_images = os.path.join(tmp_dir, oname, 'images')
        dst_dir_images = os.path.join(lng_dir, '.share/images')
        src_dir_share = os.path.join(tmp_dir, oname, 'share')
        dst_dir_share = os.path.join(lng_dir, '.share')
        src_dir_audio = os.path.join(tmp_dir, oname)
        dst_dir_audio = tpc_dir
        
        if cont == True:
            self.download(tar_url, tmp_dir, oname)
            self.manag_files(src_dir_images, dst_dir_images)
            self.manag_files(src_dir_share, dst_dir_share)
            self.manag_files(src_dir_atth, dst_dir_atth)
            self.manag_files(src_dir_audio, dst_dir_audio)
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
    

    def download(self, url, tmp_dir, oname):
        os.chdir(tmp_dir)
        files = oname + ".tar.gz"
        try:
            req = request.urlopen(url)
            with open(files, 'wb') as fp:
                shutil.copyfileobj(req, fp)
        except:
            cont = False
            print "Error on download tar"

        try: 
            opener, mode = tarfile.open, 'r:gz'
            myfiles = opener(files, mode)
            myfiles.extractall()
        except:
            cont = False
            print "Error on extract tar"
    
    def manag_files(self, src_dir, dst_dir):
        if os.path.exists(src_dir):
            try:
                for file_ in os.listdir(src_dir):
                    
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.isdir(src_file):
                        pass
                    else:
                        if not os.path.exists(dst_file):
                            shutil.move(src_file, dst_dir)
            except:
                print "Error on copying files to " + dst_dir
                pass
                
            shutil.rmtree(src_dir)
            
if __name__ == "__main__":
    downloadFiles()
