import datetime

from django.contrib.auth import login, authenticate

from simple_voting.forms import UserRegistrationForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from simple_voting.forms import Complain, VotingForm, OptionForm, VoteFormCheckBox
from .models import *

from django.db.models import Count

def index(request):
    context = {}
    context['data'] = datetime.datetime.now()

    return render(request, 'index.html', context)


def available_voting(request):
    context = {}
    context['data'] = datetime.datetime.now()
    context['votings'] = Voting.objects.all()
    context['user'] = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        print(request.POST.get('id'))
        return redirect('/vote?voting={}'.format(request.POST.get('id')))

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
                author=User.objects.get(id=request.user.id),
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

    context['option_list'] = Option.objects.filter(voting=Voting.objects.get(id=id_voting))

    if request.POST.get('status') == 'Save':
        if id_voting > 0:
            del request.session['id_voting']
        return redirect('/')

    return render(request, 'edit_voting.html', context)


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


@login_required()
def vote(request):
    context = {}
    voting_id = None
    choices = []
    form_vote = VoteFormCheckBox(request.POST)

    if request.method == 'POST':
        options = dict(form_vote.data).get('items')
        if options is not None:
            if len(options) > 0:
                for option in options:
                    print(option)
                    item = Vote(
                        option_id=Option.objects.get(id=option),
                        author_id=User.objects.get(id=request.user.id)
                    )
                    item.save()
    if len(request.GET) > 0 and request.method == 'GET':
        voting_id = request.GET.get('voting', 'error')
        if voting_id == 'error':
            return redirect('/')

        voting = Voting.objects.filter(id=voting_id)[0]
        context['question'] = voting.question
        context['description'] = voting.description
        if context['description'] is None:
            context['description'] = 'Отсутствует'

        options = Option.objects.filter(voting=voting_id)
        for i in range(len(options)):
            choices.append(('{}'.format(options[i].id), '{}'.format(options[i].text)))

        form_vote.fields['items'].choices = choices
        print(form_vote.fields['items'].choices)
        context['form_vote'] = form_vote

    if len(request.GET) == 0:
        return redirect('/')

    return render(request, 'vote.html', context)

@login_required()
def dashboard(request):
    context = {}
    voting_items = Voting.objects.filter(author_id=User.objects.get(id=request.user.id))
    context['voting_items'] = voting_items
    context['user'] = User.objects.get(id=request.user.id)

    return render(request, 'dashboard.html', context)