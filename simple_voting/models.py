from django.db import models
from django.contrib.auth.models import User


class Voting(models.Model):
    question = models.CharField(max_length=255)
    author = models.IntegerField(null=False, default=0) #TODO: Сменить на форейнки для стандартного юзера
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def options(self):
        return Option.objects.filter(voting=self)


class Option(models.Model):
    text = models.CharField(max_length=50)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)




