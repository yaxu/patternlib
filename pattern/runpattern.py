#!/usr/bin/env python

import os
import requests
from subprocess import Popen, PIPE, STDOUT

from django.conf import settings

def render_and_upload(pattern):
    code = code.decode('unicode_escape').encode('ascii', 'ignore')
    response = ""

    p = Popen([settings.RUNPATTERN_BIN],
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    tidal = p.communicate(input=code)[0]

    if p.returncode == 0:
        clyp_file_upload_url = 'http://upload.clyp.it/upload'
        cyclefile = open(os.path.join(settings.RUNPATTERN_DIR,
                                      'cycle.wav'), 'rb')
        send_files = {
            'audioFile': ('cycle.wav', cyclefile, 'audio/wav'),
            'description': code
        }
        r = requests.post(clyp_file_upload_url, files=send_files)
        if r.status_code == 200:
            response = r.json()['Url']
        else:
            response = "Sorry there's a problem uploading the pattern"
    else:
        response = "Sorry there's something wrong with that pattern: {}"

    return response
