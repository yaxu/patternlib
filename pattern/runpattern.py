#!/usr/bin/env python

import os
import requests
from subprocess import Popen, PIPE, STDOUT

from django.conf import settings

def uniqid():
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    return uniqid

def render_and_upload(code):
    code = code.decode('unicode_escape').encode('ascii', 'ignore')
    response = ""

    fnid = uniqid()
    fn = uniqid() + ".mp3"
    path = e.sub(r"(..)", r'\1/', fnid)
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
