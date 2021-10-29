from django.contrib import admin
from django.db import models

# Register your models here.
from .models import SpotReview, SurfSpot



class ChoiceInLine(admin.TabularInline):
    model = SpotReview
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'],'classes':['collapse']}),
        
    ]

    inlines = [ChoiceInLine]

    list_display = ('name', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']

    search_fields = ['name']

admin.site.register(SurfSpot, QuestionAdmin)

