from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['user']
        model = Profile