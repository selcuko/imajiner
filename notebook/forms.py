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
    
    def clean_title(self):
        title = self.cleaned_data['title']
        return title if title else _('[Entitled Narrative]')
