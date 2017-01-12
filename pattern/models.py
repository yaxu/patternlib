from django.db import models
from django.utils import timezone

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
    def __str__(self):
        return self.name
    
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

