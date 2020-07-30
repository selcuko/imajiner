from django.forms import ModelForm
from .models import Narrative


class NarrativeWrite(ModelForm):
    class Meta:
        model = Narrative
        fields = [
            'title',
            'body',
        ]