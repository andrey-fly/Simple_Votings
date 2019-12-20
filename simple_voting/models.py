from django.db import models


class Voting(models.Model):
    question = models.CharField(max_length=255)
    author = models.IntegerField(null=False, default=0)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def options(self):
        return Option.objects.filter(voting=self)


class Option(models.Model):
    text = models.CharField(max_length=50)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)



