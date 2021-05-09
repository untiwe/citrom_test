from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')


class FileFieldForm(forms.Form):
    name = forms.CharField()
    photos = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}))