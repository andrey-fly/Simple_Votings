import datetime

from django.contrib.auth import login, authenticate
from simple_voting.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from simple_voting.forms import Complain
from .models import *


def index(request):
    context = {}
    context['data'] = datetime.datetime.now()

    return render(request, 'index.html', context)


def available_voting(request):
    context = {}
    context['data'] = datetime.datetime.now()

    context['votings'] = Voting.objects.all()

    return render(request, 'available_voting.html', context)


def complain(request):
    context = {}
    if request.method == 'POST':
        cmpl = Complain(request.POST)
        if cmpl.is_valid():
            context['username'] = cmpl.username
            context['complain_type'] = cmpl.complain_type
            context['description'] = cmpl.description
            context['date'] = cmpl.date
            context['form'] = cmpl
        else:
            context['form'] = cmpl

    return render(request, 'complain.html', context)


def design(request):
    context = {}

    return render(request, 'design.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
