from django import forms


class Complain(forms.Form):
    username = forms.IntegerField(label='Your username: ', required=True)
    complain_type = forms.IntegerField(label='Your complain type: ', required=True)
    description = forms.IntegerField(label='Describe your problem: ', required=False)
    date = forms.DateField(label='Date: ')


class VotingForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        min_length=5,
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'})

    )
    description = forms.CharField(
        label = 'Дополнительное описание',
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )


class OptionForm(forms.Form):
    option = forms.CharField(
        label='Ответ',
        required=True
    )