import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from simple_voting.forms import Complain, VotingForm, OptionForm
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
            return edit_voting(request)
            # return render(request, 'edit_voting.html', context)
    return render(request, 'create_voting.html', context)


def edit_voting(request):
    voting_form = VotingForm(request.POST)
    print(voting_form.data['question'])
    print(request)
    context = {}
    option_form = OptionForm(request.POST)

    question = request.GET.get('question', 'error')

    user = request.user.id;
    votings = Voting.objects.all().values('id', 'created').filter(author=user)
    # print(user)
    # print(votings)

    voting = {}
    voting['question'] = question
    voting['description'] = 'description description description description'

    option = {}
    option['form'] = option_form


    context['voting'] = voting
    context['option'] = option
    return render(request, 'edit_voting.html', context)
