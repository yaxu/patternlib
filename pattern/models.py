from django.db import models
from django.utils import timezone
from pattern.tasks import run_render_and_upload

import ws

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
    
class Pattern(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey('Identity')
    language = models.ForeignKey('Language')
    code = models.TextField()
    history = models.TextField(null=True)
    url = models.URLField(blank=True, null=True)
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


def render_pattern(sender, instance, using, **kwargs):
    models.signals.post_save.disconnect(render_pattern, sender=sender)

    url = run_render_and_upload(instance.code)
    instance.url = url
    instance.save()

    models.signals.post_save.connect(render_pattern, sender=sender)

models.signals.post_save.connect(render_pattern, sender=Pattern)
