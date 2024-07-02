from django import forms
from .models import Thread, Reply

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']