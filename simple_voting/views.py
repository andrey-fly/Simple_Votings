import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from simple_voting.forms import Complain, VotingForm, OptionForm, VoteFormCheckBox
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


@login_required()
def create_voting(request):
    context = {}
    voting_form = VotingForm(request.POST)
    context['voting_form'] = voting_form
    if request.method == 'POST':
        if voting_form.is_valid():
            item = Voting(
                question=voting_form.data['question'],
                author=request.user.id,
                description=voting_form.data['description'])

            data = Voting.objects.all().values('question', 'author')
            for row in data:
                if row['question'] == voting_form.data['question'] and row['author'] == request.user.id:
                    error = dict()
                    error['message'] = 'Вы уже создали опрос с таким названием'
                    error['question'] = voting_form.data['question']
                    context['error'] = error
                    return render(request, 'create_voting.html', context)

            item.save()
            request.session['id_voting'] = item.id
            return edit_voting(request)
            # return render(request, 'edit_voting.html', context)
    return render(request, 'create_voting.html', context)


def edit_voting(request):
    context = {}

    id_voting = request.session.get('id_voting', -1)
    user = request.user.id

    option_form = OptionForm(request.POST)
    if request.method == 'POST' and id_voting > 0:
        if option_form.is_valid():
            item = Option(text=option_form.data['option'], voting=Voting.objects.get(id=id_voting))
            item.save()

    if id_voting > 0:
        voting = Voting.objects.all().filter(id=id_voting).values('question', 'description')
        question = voting[0]['question']
        description = voting[0]['description']
    else:
        question = 'question'
        description = 'description'

    voting_context = {}
    voting_context['question'] = question
    voting_context['description'] = description

    option_context = {}
    option_context['form'] = option_form

    context['voting'] = voting_context
    context['option'] = option_context

    if request.POST.get('status') == 'Save':
        if id_voting > 0:
            del request.session['id_voting']
        return redirect('/')

    return render(request, 'edit_voting.html', context)


@login_required()
def vote(request):
    context = {}

    if len(request.GET) == 0:
        return redirect('/')
    else:
        voting_id = request.GET.get('voting', 'error')
        if voting_id == 'error':
            return redirect('/')
        voting = Voting.objects.all().filter(id=voting_id).values('question', 'description', 'author')
        voting = voting[0]
        if voting['description'] is None:
            voting['description'] = 'Отсутствует'
        context['voting'] = dict([('question', voting['question']),('description', voting['description'])])

        context['options'] = Option.objects.all().filter(voting=voting_id)

    form = VoteFormCheckBox(request.POST)
    context['choice_form'] = form


    return render(request, 'vote.html', context)
