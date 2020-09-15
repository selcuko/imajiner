from django import forms
from django.utils import html
from .models import Narrative, SoundRecord

class ButtonWidget(forms.Widget):
    def render(self, id="button", name="", renderer=None, value="Entitled Button", attrs=None):
        return f'<button name="{html.escape(id)}">{html.escape(value)}"</button>'

class NarrativeForm(forms.ModelForm):
    class Meta:
        model = Narrative
        fields = [
            'uuid',
            'title',
            'body',
            'sound',
        ]

        widgets = {
            'uuid': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'full-width'}),
            'body': forms.Textarea(attrs={'class': 'full-width'}),
            'sound': ButtonWidget(),#forms.ButtonWidget(attrs={'class': 'full-width'}),
        }

        labels = {
            'title': 'Önden gelen tekst',
            'body': 'Asıl yazı',
            'sound': 'Eklemek istersen ses',
        }

class SoundUploadForm(forms.ModelForm):
    class Meta:
        model = SoundRecord
        fields = [
            'name',
            'file',
        ]
        