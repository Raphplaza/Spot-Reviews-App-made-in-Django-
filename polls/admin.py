from django.contrib import admin
from django.db import models

# Register your models here.
from .models import SpotReview, SpotName


#admin.site.register(Question)

class ChoiceInLine(admin.TabularInline):
    model = SpotReview
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],'classes':['collapse']}),
        
    ]

    inlines = [ChoiceInLine]

    list_display = ('question_text', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']

    search_fields = ['question_text']

admin.site.register(SpotName, QuestionAdmin)

