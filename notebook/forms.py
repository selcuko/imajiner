from django import forms
from django.utils import html
from django.utils.translation import gettext_lazy as _
from .models import NarrativeTranslation

class NarrativeForm(forms.ModelForm):
    class Meta:
        model = NarrativeTranslation
        fields = [
            'uuid',
            'title',
            'body',
        ]

        widgets = {
            'uuid': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'full-width'}),
            'body': forms.Textarea(attrs={'class': 'full-width'}),
        }

        labels = {
            'title': _('Title'),
            'body': _('Body'),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        return title if title else _('[Entitled Narrative]')
