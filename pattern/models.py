from django.db import models
from django.utils import timezone
from tasks import run_render_and_upload

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Pattern(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User')
    language = models.ForeignKey('Language')
    code = models.TextField()
    history = models.TextField(null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    pattern = models.ForeignKey('Pattern')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.author.name


def render_pattern(sender, instance, using, **kwargs):
    url = run_render_and_upload(instance.code)
    instance.url = url
    instance.save()

post_save.connect(render_pattern, sender=Pattern)
