from django import forms
from django.utils import html
from django.utils.translation import gettext_lazy as _
from .models import Narrative, SoundRecord

class NarrativeForm(forms.ModelForm):
    class Meta:
        model = Narrative
        fields = [
            'uuid',
            'title',
            'body',
        ]

        widgets = {
            'uuid': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'philosophy full-width'}),
            'body': forms.Textarea(attrs={'class': 'philosophy full-width'}),
        }

        labels = {
            'title': _('title').capitalize(),
            'body': _('body').capitalize(),
        }

class SoundUploadForm(forms.ModelForm):
    class Meta:
        model = SoundRecord
        fields = [
            'name',
            'file',
        ]
