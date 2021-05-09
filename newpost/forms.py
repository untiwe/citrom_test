from django import forms
from mymodels.models import PostsPhotos


class PhotoForm(forms.ModelForm):

    photo = forms.FileField()
    # required=False
    
    class Meta:
        model = PostsPhotos
        fields = ('photo',)
