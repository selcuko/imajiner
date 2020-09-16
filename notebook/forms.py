from django import forms
from django.utils import html
from .models import Narrative, SoundRecord

class ButtonWidget(forms.Widget):
    def render(self, id="button", name="", renderer=None, value="Entitled Button", attrs=None):
        return f'<button class="ui button" id="{html.escape(id)}">{value}"</button>'

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
            'title': forms.TextInput(attrs={'class': 'full-width'}),
            'body': forms.Textarea(attrs={'class': 'full-width'}),
        }

        labels = {
            'title': 'Önden gelen tekst',
            'body': 'Asıl yazı',
        }

class SoundUploadForm(forms.ModelForm):
    class Meta:
        model = SoundRecord
        fields = [
            'name',
            'file',
        ]
        