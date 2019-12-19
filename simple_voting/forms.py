from django import forms


class Complain(forms.Form):
    username = forms.IntegerField(label='Your username: ', required=True)
    complain_type = forms.IntegerField(label='Your complain type: ', required=True)
    description = forms.IntegerField(label='Describe your problem: ', required=False)
    date = forms.DateField(label='Date: ')


class Voting(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        min_length=1,
        max_length=100,
        required=True
    )


class Option(forms.Form):
    option = forms.CharField(
        label='Ответ',
        required=True
    )