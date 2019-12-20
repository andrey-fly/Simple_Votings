from django import forms


class Complain(forms.Form):
    username = forms.IntegerField(label='Your username: ', required=True)
    complain_type = forms.IntegerField(label='Your complain type: ', required=True)
    description = forms.IntegerField(label='Describe your problem: ', required=False)
    date = forms.DateField(label='Date: ')


class LogInForm(forms.Form):
    username = forms.CharField(label='Login: ', required=True)
    password = forms.CharField(label='Password: ', required=True)
