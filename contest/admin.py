from django.contrib import admin
from contest import forms, models

class ContestAdmin(admin.ModelAdmin):
    form = forms.ContestForm

admin.site.register(models.Contest, ContestAdmin)
