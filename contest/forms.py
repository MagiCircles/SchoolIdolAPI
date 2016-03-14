from django import forms
from dal import autocomplete
from api import models as api_models
from contest import models

class ContestForm(forms.ModelForm):
    suggested_by_username = forms.CharField(required=False)
    image_by_username = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.suggested_by:
            self.fields['suggested_by_username'].initial = self.instance.suggested_by.username
        if self.instance and self.instance.image_by:
            self.fields['image_by_username'].initial = self.instance.image_by.username

    def save(self, commit=False):
        instance = super(ContestForm, self).save(commit=False)
        if self.cleaned_data['suggested_by_username']:
            try: instance.suggested_by = api_models.User.objects.get(username=self.cleaned_data['suggested_by_username'])
            except: instance.suggested_by = None
        if self.cleaned_data['image_by_username']:
            try: instance.image_by = api_models.User.objects.get(username=self.cleaned_data['image_by_username'])
            except: instance.image_by = None
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Contest
        fields = ('__all__')
        exclude = ('suggested_by', 'image_by')
