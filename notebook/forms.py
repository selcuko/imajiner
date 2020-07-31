from django import forms
from .models import Narrative


class NarrativeWrite(forms.ModelForm):
    class Meta:
        model = Narrative
        fields = [
            'title',
            'body',
            #'uuid',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'full-width'}),
            'body': forms.Textarea(attrs={'class': 'full-width'}),
        }
        