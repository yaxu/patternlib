from django.db import models
from django.utils import timezone
from pattern.tasks import run_render_and_upload
from django.conf import settings

import ws
import os

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    
class Identity(models.Model):
    name = models.CharField(max_length=200)
    ident = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', null=True)
    # null if it's a local user
    service = models.ForeignKey('Service', null=True)
    def __str__(self):
        return self.ident

class Pattern(models.Model):
    name = models.CharField(max_length=200)
    loves = models.ManyToManyField(Identity, related_name="pattern_loves")
    author = models.ForeignKey('Identity')
    language = models.ForeignKey('Language')
    parent = models.ForeignKey('self', null=True)
    code = models.TextField()
    history = models.TextField(null=True)
    audiourl = models.URLField(blank=True, null=True)
    errorMessage = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices = (
            ('error', 'Error'),
            ('editing', 'Editing'),
            ('pending', 'Pending'),
            ('rendering', 'Rendering'),
            ('live', 'Live'),
        )
    )
    
    def __str__(self):
        return self.name

    def lovePattern(self, user):
        self.loves.add(user)

    def unlovePattern(self, user):
        print("unlove")
        self.loves.remove(user)

    def typecheck(self):
        result = ws.sendrecv("/typecheck " + self.code)
        print(result[1])
        if (result[1] == 'ok'):
            self.status = 'pending'
            return(True)
        else:
            if (result[1] == 'nok'):
                self.status = 'error'
                print("static: "  + result[1])
                print("error: "  + result[2])
                self.errorMessage = result[2]
                return(False)

    def render(self):
        filename = str(self.id)
        filepath_tmp = os.path.join(settings.PATTERN_QUEUEDIR, filename + ".tmp")
        filepath = os.path.join(settings.PATTERN_QUEUEDIR, filename + ".tidal")
        f = open(filepath_tmp, "w")
        f.write(self.code)
        f.close()
        os.rename(filepath_tmp, filepath)
        self.audiourl = os.path.join(settings.PATTERN_AUDIOURL,
                                     settings.PATTERN_GENPATH(filename),
                                     filename + ".mp3"
                                    )
        self.status = 'rendering'

    def is_live(self):
        result = False
        if self.status == 'live':
            result = True
        elif self.status == 'rendering':
            filepath = os.path.join(settings.PATTERN_AUDIODIR, self.audiourl)
            print "test " + filepath
            if os.path.isfile(filepath):
                result = True
                self.status = 'live'
                self.save()
        return result
    
class Comment(models.Model):
    pattern = models.ForeignKey('Pattern')
    author = models.ForeignKey('Identity')
    # the end state of the code
    text = models.TextField()
    # livewriting recording
    writing = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.author.name

