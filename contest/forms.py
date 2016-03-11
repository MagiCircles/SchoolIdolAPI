from django import forms
from dal import autocomplete
from contest import models

class ContestForm(forms.ModelForm):
    class Meta:
        model = models.Contest
        fields = ('__all__')
        widgets = {
            'suggested_by': autocomplete.ModelSelect2(url='autocomplete-user'),
            'image_by': autocomplete.ModelSelect2(url='autocomplete-user'),
        }
