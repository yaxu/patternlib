from django import forms
from .models import Pattern

class PatternForm(forms.ModelForm):

    class Meta:
        model = Pattern
        fields = ('name', 'code')
