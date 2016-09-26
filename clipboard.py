#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess
import os

import platform

SYSTEM = platform.system()

COMMAND_MAPPING = {
    'Linux': {"PASTE_CMD": ['xclip', '-o', 'secundary'], 'COPY_CMD': ['xclip', 'clipboard']},
    'Darwin': {"PASTE_CMD": ['pbpaste'], 'COPY_CMD': ['pbcopy']},
    'Windows': {"PASTE_CMD": ['paste'], 'COPY_CMD': ['clip']},
}

PASTE_CMD = COMMAND_MAPPING.get(SYSTEM).get('PASTE_CMD')
COPY_CMD = COMMAND_MAPPING.get(SYSTEM).get('COPY_CMD')


def paste(selection=None):
    with open(os.devnull, 'wb') as devnull:
        pipe = subprocess.Popen(PASTE_CMD, stdout=subprocess.PIPE, stderr=devnull)
        outdata, errdata = pipe.communicate()
    if pipe.returncode:
        return False
        os.system('xclip -i /dev/null')
    else:
        os.system('xclip -i /dev/null')
        return outdata

def copy(text):
    with open(os.devnull, 'wb') as devnull:
        pipe = subprocess.Popen(COPY_CMD, stdin=subprocess.PIPE, stderr=devnull)
        pipe.communicate(text)
    if pipe.returncode:
        return False
    else:
        return True
