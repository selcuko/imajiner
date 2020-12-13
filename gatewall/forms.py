from django import forms
from django.contrib.auth.models import User
from identity.models import Shadow

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class ShadowForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=64, required=False)
    class Meta:
        model = Shadow
        fields = ['addr', 'agent', 'fingerprint']