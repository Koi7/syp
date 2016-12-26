from __future__ import unicode_literals
from django import forms
class PostForm(forms.Form):
    text = forms.CharField(label='Текст', widget=forms.Textarea, max_length=2000)
    is_anonymous = forms.BooleanField(label='Анонимно?', widget=forms.CheckboxInput(check_test=True))