from django import forms
from mymodels.models import AdminMessages


class AdminMessagesForm(forms.ModelForm):
    '''Класс формы для обратной связи'''

    class Meta:
        model = AdminMessages
        fields = ['user_username', 'name', 'contacts', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text_input'}),
            'contacts': forms.TextInput(attrs={'class': 'text_input'}),
            'text': forms.Textarea(attrs={'rows':3, 'cols':10}),
        } 

        