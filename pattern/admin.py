from django import forms
from django.contrib import admin

from .widgets import CodeEditor
from .models import *


class PatternAdminForm(forms.ModelForm):
    model = Pattern
    class Meta:
        fields = '__all__'
        widgets = {
          'code': CodeEditor(attrs={'style': 'width: 90%; height: 100%'})
        }

class PatternAdmin(admin.ModelAdmin):
    form = PatternAdminForm
admin.site.register(Pattern, PatternAdmin)
