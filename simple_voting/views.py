import datetime

from django.contrib.auth import login, authenticate
from django.template.context_processors import csrf
from django.views import View

from simple_voting.forms import UserRegistrationForm

from django.shortcuts import render, redirect

from simple_voting.forms import Complain
from simple_votings_11 import settings
from .models import *

from django.views import View
from django.core.mail import send_mail


def index(request):
    context = {}
    context['data'] = datetime.datetime.now()

    return render(request, 'index.html', context)


def available_voting(request):
    context = {}
    context['data'] = datetime.datetime.now()

    context['votings'] = Voting.objects.all()

    return render(request, 'available_voting.html', context)


# def complain(request):
#     context = {}
#     if request.method == 'POST':
#         cmpl = Complain(request.POST)
#         if cmpl.is_valid():
#             context['username'] = cmpl.username
#             context['complain_type'] = cmpl.complain_type
#             context['description'] = cmpl.description
#             context['date'] = cmpl.date
#             context['form'] = cmpl
#         else:
#             context['form'] = cmpl
#
#     return render(request, 'complain.html', context)


def design(request):
    context = {}

    return render(request, 'design.html', context)


def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password2'])
            # Save the User object
            new_user.save()
            return render(request, 'index.html', {'username': user_form.data['username']})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def complain(request):
    context = {}

    if request.method == 'GET':
        context.update(csrf(request))
        context['complain_form'] = Complain()

        return render(request, 'complain.html', context)
    elif request.method == 'POST':

        form = Complain(request.POST)
        if form.is_valid():
            email_subject = 'EVILEG :: Сообщение через контактную форму '
            email_body = "С сайта отправлено новое сообщение\n\n" \
                         "Имя отправителя: %s \n" \
                         "E-mail отправителя: %s \n\n" \
                         "Сообщение: \n" \
                         "%s " % \
                         (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])

            # данный код можно будет использовать, когда станет возможным отправлять сообщения на сервер и на почту
            # send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['target_email@example.com'],
            #           fail_silently=False)

    return render(request, 'complain.html', context)
