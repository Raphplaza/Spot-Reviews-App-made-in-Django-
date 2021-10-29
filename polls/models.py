
from time import time
from django.contrib import admin
from django.contrib.admin import decorators
from django.db import models

from datetime import timedelta
from django.utils import timezone



class SpotName(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return (self.question_text)

#decorator for display purposes
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - timedelta(days=1)

class SpotReview(models.Model):
    question = models.ForeignKey(SpotName, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text