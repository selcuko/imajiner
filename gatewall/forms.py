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


class ShadowForm(forms.Form):
    class Meta:
        model = Shadow
        fields = ['username']