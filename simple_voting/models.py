from django.db import models
from django.contrib.auth.models import User


class Voting(models.Model):
    question = models.CharField(max_length=255)
    author = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)

    def options(self):
        return Option.objects.filter(voting=self)

    def likes(self):
        return Like.objects.filter(voting=self)

    def comments(self):
        return Comment.objects.filter(voting=self)


class Option(models.Model):
    text = models.CharField(max_length=50)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vote_count = models.IntegerField(default=0)

    def votes(self):
        return Vote.objects.filter(option=self)


class Vote(models.Model):
    option = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
