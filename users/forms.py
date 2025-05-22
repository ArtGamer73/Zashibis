from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import Form, EmailInput, CharField, PasswordInput, TextInput, ChoiceField, ModelChoiceField, Select
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Come up with a password',
            'id': 'id_password1',
            'data-toggle': 'password',
        })
    )

    class Meta:
        model =  User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control email',
                'placeholder': 'Name',
            }),
        }

class EmailPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))



from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
