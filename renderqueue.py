#!/usr/bin/env python

import pyinotify
import os
from os.path import join, getsize
from glob import glob
import time
import math
import re
from subprocess import Popen, PIPE, STDOUT
import errno

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patternsite.settings")

from django.conf import settings

def uniqid():
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    return uniqid

def render(fnid, code):
    code = code.decode('unicode_escape').encode('ascii', 'ignore')
    response = ""

    fn = fnid + ".mp3"
    tmpfn = fnid + "-rendering.mp3"
    path = settings.PATTERN_GENPATH(fnid)
    fullpath = os.path.join(settings.PATTERN_AUDIODIR,
                            settings.PATTERN_AUDIOURL,
                            path)
    
    try:
        print("making " + fullpath)
        os.makedirs(fullpath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    abspath = os.path.join(fullpath, fn)
    abstmppath = os.path.join(fullpath, tmpfn)

    p = Popen([settings.RUNPATTERN_BIN, abstmppath],
               stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    tidal = p.communicate(input=code)[0]

    if p.returncode == 0:
        os.rename(abstmppath,abspath)

    return(p.returncode == 0)

def process():
    filepaths = glob(os.path.join(settings.PATTERN_QUEUEDIR, '*.tidal'))
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        name = re.match(r'(.*?)\.', filename).group(1)
        f = open(filepath, "r")
        code = f.read()
        print(code)
        f.close()
        if render(name, code):
            print "success"
            # maybe should be saved/logged..
            os.unlink(filepath)
        else:
            print "error"
            os.rename(filepath,os.path.join(settings.PATTERN_QUEUEDIR_ERROR,filename))
        
def watch():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MOVED_TO
    
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_MOVED_TO(self, event):
            process()

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(settings.PATTERN_QUEUEDIR, mask)
    notifier.loop()

process()
watch()
