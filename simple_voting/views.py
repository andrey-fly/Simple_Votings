import datetime

from django.contrib.auth import login, authenticate
from django.template.context_processors import csrf
from django.views import View

from simple_voting.forms import *

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from simple_voting.forms import Complain, VotingForm, OptionForm, VoteFormCheckBox
from simple_votings_11 import settings
from .models import *
from django.db.models import Count
from django.views import View
from django.core.mail import send_mail


def index(request):
    clear_session(request)
    context = {}
    context['data'] = datetime.datetime.now()

    return render(request, 'index.html', context)


def available_voting(request):
    clear_session(request)
    context = {}
    context['data'] = datetime.datetime.now()
    context['votings'] = Voting.objects.all()
    context['user'] = User.objects.get(id=request.user.id)

    counting_index = 0
    for option in Option.objects.all():
        option.vote_count = option.votes().count()
        counting_index += 1
        option.save()
    context['options'] = Voting.objects.all()

    if request.method == 'POST':
        print(request.POST.get('id'))
        return redirect('/vote?voting={}'.format(request.POST.get('id')))

    return render(request, 'available_voting.html', context)


def design(request):
    clear_session(request)
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
            return generate_voting(request)
            # return render(request, 'generate_voting.html', context)
    return render(request, 'create_voting.html', context)


def generate_voting(request):
    context = {}

    id_voting = request.session.get('id_voting', -1)

    option_form = OptionForm(request.POST)
    if request.method == 'POST' and id_voting > 0:
        if option_form.is_valid():
            item = Option(text=option_form.data['option'], voting=Voting.objects.get(id=id_voting))
            item.save()
            return redirect('/generate_voting/')

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
        return redirect('/available_voting')

    return render(request, 'generate_voting.html', context)


def signup(request):
    clear_session(request)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password2'])
            # Save the User object
            new_user.save()
            login(request, new_user)
            return render(request, 'index.html', {'username': user_form.data['username']})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def complain(request):
    context = {}
    clear_session(request)
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


@login_required()
def vote(request):
    clear_session(request)
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
                        option=Option.objects.get(id=option),
                        author=User.objects.get(id=request.user.id)
                    )
                    item.save()
    if len(request.GET) > 0 and request.method == 'GET':
        voting_id = request.GET.get('voting', 'error')
        if voting_id == 'error':
            return redirect('/available_voting')
        voting = Voting.objects.get(id=voting_id)
        opts = Option.objects.filter(voting=voting)
        for item in opts:
            vts = item.votes()
            for jtem in vts:
                username = User.objects.get(id=request.user.id).username
                if jtem.author.username == username:
                    context['error'] = "You are already voted"
                    print(context['error'])
                    return render(request, 'vote.html', context)

        voting = Voting.objects.filter(id=voting_id)[0]
        context['question'] = voting.question
        context['description'] = voting.description
        if context['description'] is None:
            context['description'] = 'Отсутствует'

        options = Option.objects.filter(voting_id=voting_id)
        for i in range(len(options)):
            choices.append(('{}'.format(options[i].id), '{}'.format(options[i].text)))

        form_vote.fields['items'].choices = choices
        print(form_vote.fields['items'].choices)
        context['form_vote'] = form_vote

    if len(request.GET) == 0:
        return redirect('/available_voting')

    return render(request, 'vote.html', context)


@login_required()
def profile(request):
    clear_session(request)
    context = {}
    voting_items = Voting.objects.filter(author_id=User.objects.get(id=request.user.id))
    context['voting_items'] = voting_items
    context['user'] = User.objects.get(id=request.user.id)

    return render(request, 'profile.html', context)

@login_required()
def change_info(request):
    clear_session(request)
    form = ChangeInfoForm(request.POST)
    context = {}
    context['form'] = form
    current_user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        if request.POST.get('old_password'):
            old_password = request.POST.get('old_password')
            if current_user.check_password('{}'.format(old_password)) is False:
                form.set_old_password_flag()
                return render(request, 'change_info.html', {'form': form})
        if form.is_valid():
            if request.POST.get('username'):
                current_user.username = request.POST.get('username')
            if request.POST.get('first_name'):
                current_user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name'):
                current_user.last_name = request.POST.get('last_name')
            if request.POST.get('email'):
                current_user.email = request.POST.get('email')
            if request.POST.get('old_password'):
                old_password = request.POST.get('old_password')
                if current_user.check_password('{}'.format(old_password)) is False:
                    form.set_old_password_flag()
                    return render(request, 'change_info.html', {'form': form})
                else:
                    current_user.set_password('{}'.format(form.data['new_password2']))
            current_user.save()
            login(request, current_user)
        else:
            return render(request, 'change_info.html', context)
    if request.POST.get('status') == 'Save':
        return redirect('/profile')
    return render(request, 'change_info.html', context)


@login_required()
def edit_voting(request):
    context = {}

    voting_form = EditVotingForm(request.POST)
    context['voting_form'] = voting_form
    option_form = OptionForm(request.POST)
    context['option_form'] = option_form

    if request.method == 'POST':
        if request.session.get('id_voting', 'error') == 'error':
            votes_id = request.POST
            for vid in votes_id:
                vote_id = vid
            request.session['id_voting'] = vote_id

        vote_id = request.session.get('id_voting', 'error')
        print(vote_id)

        if voting_form.is_valid():
            new_question = voting_form.cleaned_data.get('question')
            new_desc = voting_form.cleaned_data.get('description')

            voting = Voting.objects.get(id=vote_id)

            if new_question:
                voting.question = new_question
                voting.save()

            if new_desc:
                voting.description = new_desc
                voting.save()

        options = Option.objects.filter(voting=Voting.objects.get(id=vote_id))
        context['options'] = options
        delete = request.POST.get('Delete')
        if delete:
            Option.objects.get(id=delete).delete()

        if option_form.is_valid():
            new_option = option_form.data['option']
            new_option = Option(text=new_option, voting=Voting.objects.get(id=vote_id))
            new_option.save()

        if request.POST.get('status') == 'GO BACK':
            return redirect('../profile')

        if request.POST.get('status') == 'DELETE':
            Voting.objects.get(id=vote_id).delete()
            print("DONE")
            return redirect('/profile/')

    return render(request, 'edit_voting.html', context)


def clear_session(request):
    if request.session.get('id_voting', None):
        del request.session['id_voting']