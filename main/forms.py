from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserCreadential_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'email' : forms.TextInput(attrs={}),
            'password' : forms.PasswordInput(attrs={})
        }

class UserProfile_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name' : forms.TextInput(attrs={}),
            'last_name' : forms.TextInput(attrs={}),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'email' : forms.TextInput(attrs={'id' : 'user_email'}),
            'password' : forms.PasswordInput(attrs={'id' : 'user_password'})
        }


class UrlForm(forms.Form):
    url = forms.CharField(label='URL:', max_length=400)


class Search(forms.Form):
    search = forms.CharField(label='', max_length=400, initial=' ')