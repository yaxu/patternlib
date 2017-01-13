from django import forms
from django.contrib import admin
from models import (
    Language,
    Pattern,
    Comment
)

from .widgets import CodeEditor
from .models import *

class PatternAdminForm(forms.ModelForm):
    model = Pattern
    class Meta:
        fields = '__all__'
        widgets = {
          'code': CodeEditor(attrs={'style': 'width: 90%; height: 100%'})
        }

class LanguageAdmin(admin.ModelAdmin):
    pass

class PatternAdmin(admin.ModelAdmin):
    form = PatternAdminForm

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Comment, CommentAdmin)