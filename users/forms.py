from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import Form, EmailInput, CharField, PasswordInput, TextInput, ChoiceField, ModelChoiceField, Select
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Придумайте пароль',
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

class EmailPasswordForm(Form):
    username = CharField(
        label="Username", 
        widget=TextInput(attrs={
            'class': 'form-control email',
            'placeholder': 'User',
        }),
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Passw0rd',
            'id': 'id_password',
            'data-target': 'id_password'
        }),
        label="Password"
    )
