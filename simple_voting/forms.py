from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Complain(forms.Form):
    username = forms.IntegerField(label='Your username: ', required=True)
    complain_type = forms.IntegerField(label='Your complain type: ', required=True)
    description = forms.IntegerField(label='Describe your problem: ', required=False)
    date = forms.DateField(label='Date: ')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
