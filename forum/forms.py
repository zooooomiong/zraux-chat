from django import forms
from .models import OrdinaryUser, Messages

class UserForm(forms.ModelForm):
    
    class Meta:
        model = OrdinaryUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class MessageForm(forms.ModelForm):
    message = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    
    class Meta:
        model = Messages
        fields = ['message']
