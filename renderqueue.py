#!/usr/bin/env python

import pyinotify
import os
from os.path import join, getsize
from glob import glob
import time
import math
import re
from subprocess import Popen, PIPE, STDOUT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patternsite.settings")

from django.conf import settings

def uniqid():
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    return uniqid

def render(code):
    code = code.decode('unicode_escape').encode('ascii', 'ignore')
    response = ""

    fnid = uniqid()
    fn = uniqid() + ".mp3"
    path = re.sub(r"(..)", r'\1/', fnid)
    fullpath = os.path.join(settings.BASE_DIR, "mp3s", path)
    
    try:
        os.makedirs(fullpath)
    except e:
        if e.errno != errno.EEXIST:
            raise
        
    abspath = os.path.join(fullpath, fn)

    p = Popen([settings.RUNPATTERN_BIN, abspath],
               stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    tidal = p.communicate(input=code)[0]

    if p.returncode == 0:
        response = os.path.join("/mp3s", path, fn)
    else:
        response = "Sorry there's something wrong with that pattern: {}"

    return response

def process():
    filenames = glob(os.path.join(settings.PATTERN_QUEUEDIR, '*.tidal'))
    for filename in filenames:
        f = open(filename, "r")
        code = f.read()
        print(code)
        print render(code)
        f.close()
        os.unlink(filename)
        
def watch():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE
    
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            process()

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(settings.PATTERN_QUEUEDIR, mask)
    notifier.loop()

process()
watch()
