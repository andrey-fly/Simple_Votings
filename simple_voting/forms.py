from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Textarea
from django.forms.widgets import Input
from django.views.generic.edit import FormView

from simple_voting.models import Voting


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), min_length=8)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': Input(attrs={'class': 'form-control', 'placeholder': 'Password', 'autofocus': ''}),
            'first_name': Input(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'last_name': Input(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'email': Input(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autofocus': ''}
    # password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autofocus': ''}), min_length=8, required=True)

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_username(self):
        cd = self.data
        if len(cd['username']) < 6:
            raise forms.ValidationError('Username must have 6 or more symbols')
        return cd['username']

    def clean_email(self):
        cd = self.data
        users = User.objects.all()
        for user in users:
            if user.email == cd['email']:
                raise forms.ValidationError('This email is already in use')
        return cd['email']


class VotingForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        min_length=5,
        max_length=25,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Question', 'style': 'border-radius: 8px'})

    )
    description = forms.CharField(
        label='Дополнительное описание',
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Description', 'style': 'border-radius: 8px'})
    )
    isSingle = forms.BooleanField(
        label='Один вариант ответа',
        required=False,
    )


class OptionForm(forms.Form):
    option = forms.CharField(
        label='Ответ',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Question', 'style': 'border-radius: 8px', 'autofocus': ''})
    )


class VoteFormCheckBox(forms.Form):
    items = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, )


class LikeForm(forms.Form):
    like = forms.BooleanField(required=False, label='Добавить в избранное: ')


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Discuss this voting here:',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Description', 'style': 'border-radius: 8px'}),
        required=False
    )


class ChangeInfoForm(forms.Form):
    username = forms.CharField(label='Username', min_length=3, required=False)
    first_name = forms.CharField(label='First name', min_length=3, required=False)
    last_name = forms.CharField(label='Last name', min_length=3, required=False)
    email = forms.EmailField(label='Email', required=False)
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput, required=False, initial=None)
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8, required=False,
                                   initial=None)
    new_password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, required=False, initial=None)
    old_password_flag = True

    def set_old_password_flag(self):
        self.old_password_flag = False

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password and self.data.get('new_password'):
            print('Not')
            raise forms.ValidationError("You must enter your old password.")
        if self.old_password_flag is False:
            raise forms.ValidationError("The old password that you have entered is wrong.")
        return old_password

    def clean_new_password2(self):
        new_password = self.cleaned_data.get('new_password')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password != new_password2:
            raise forms.ValidationError('New passwords don\'t match.')
        return new_password2


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


class Question(forms.Form):
    name = forms.CharField(
        label='Your username',
        widget=forms.TextInput
    )

    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput
    )

    message = forms.CharField(
        label='Describe your question',
        widget=forms.Textarea
    )


class EditVotingForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        min_length=5,
        max_length=25,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Question', 'style': 'border-radius: 8px'})

    )
    description = forms.CharField(
        label='Дополнительное описание',
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Description', 'style': 'border-radius: 8px'})
    )

    class Meta:
        model = Voting


class RecoveryPass(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autofocus': ''}), min_length=8, required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Repeat password'}), required=True)

    class Meta:
        model = User
        fields = ()

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']