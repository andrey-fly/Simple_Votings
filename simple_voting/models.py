from django.db import models
from django.contrib.auth.models import User


class Voting(models.Model):
    question = models.CharField(max_length=255)
    author = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def options(self):
        return Option.objects.filter(voting=self)


class Option(models.Model):
    text = models.CharField(max_length=50)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)


class Vote(models.Model):
    option = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
