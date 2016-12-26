#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
class PostForm(forms.Form):
    text = forms.CharField(label=u'Текст', widget=forms.Textarea, max_length=2000)
    is_anonymous = forms.BooleanField(label=u'Анонимно?', widget=forms.CheckboxInput(check_test=True))