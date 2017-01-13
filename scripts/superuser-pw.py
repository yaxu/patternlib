#!/usr/bin/env python
import os
import sys


reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "patternsite.settings")

import django
django.setup()
from django.contrib.auth.models import User


if __name__ == "__main__":
    if len(sys.argv):
        admin = User.objects.get(username=sys.argv[1])
        admin.set_password(sys.argv[2])
        admin.save()
