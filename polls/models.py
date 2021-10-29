
from time import time
from django.contrib import admin
from django.contrib.admin import decorators
from django.db import models

from datetime import timedelta
from django.utils import timezone



class SurfSpot(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return (self.name)

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
    surfspot = models.ForeignKey(SurfSpot, on_delete = models.CASCADE)
    review_text = models.CharField(max_length=200)
    author = models.CharField(max_length=30, default="unknown author")

    def __str__(self):
        return self.review_text