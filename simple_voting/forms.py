from django import forms
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class LogInForm(forms.Form):
#     username = forms.CharField(label='Login: ', required=True)
#     password = forms.CharField(label='Password: ', required=True)


# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#
#     success_url = "/login/"
#     template_name = "register.html"
#
#     def form_valid(self, form):
#         form.save()
#
#         return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class Complain(forms.Form):
    name = forms.CharField(
        label='Your username',
        widget=forms.TextInput
    )

    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput
    )

    message = forms.CharField(
        label='Describe your problem',
        widget=forms.Textarea
    )
