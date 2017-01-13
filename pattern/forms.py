from django import forms
from .widgets import CodeEditor
from .models import Pattern


class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ('code', 'name','history')
        widgets = {
            #'code': CodeEditor(attrs={'style': 'width: 90%'}),
            'history': forms.HiddenInput(),
            'code': forms.HiddenInput()
        }
#    def clean(self):
#        name = self.cleaned_data['name']
#        code = self.cleaned_data['code']
        
