from django import forms

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'learning_log.settings')
django.setup()

from learning_logs.models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}