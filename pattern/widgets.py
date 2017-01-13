from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage

class CodeEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'code-editor'

    class Media:
        css = {
            'all': (
                staticfiles_storage.url('codemirror-5.22.0/lib/codemirror.css'),
                staticfiles_storage.url('css/edit.css'),
                staticfiles_storage.url('livewriting/livewriting.css'),
            )
        }
        js = (
            staticfiles_storage.url('codemirror-5.22.0/lib/codemirror.js'),
            staticfiles_storage.url('livewriting/index.js'),
            staticfiles_storage.url('js/livewriting-init.js'),
        )
