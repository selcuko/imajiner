from django import forms
from .models import Narrative, SoundRecord


class NarrativeWrite(forms.ModelForm):
    class Meta:
        model = Narrative
        fields = [
            'title',
            'body',
            'sound',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'full-width'}),
            'body': forms.Textarea(attrs={'class': 'full-width'}),
        }

class SoundUploadForm(forms.ModelForm):
    class Meta:
        model = SoundRecord
        fields = [
            'name',
            'file',
        ]
        