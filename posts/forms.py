#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
class PostForm(forms.Form):
    text = forms.CharField(label='Текст', widget=forms.Textarea, max_length=2000)
    is_anonymous = forms.BooleanField(required=False)
    