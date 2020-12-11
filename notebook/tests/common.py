from django.test import TestCase as TC
from django.shortcuts import reverse
from model_bakery import baker
from ..models import NarrativeTranslation

class TestCase(TC):
    @classmethod
    def setUpTestData(cls): 
        cls.user = baker.make('auth.User')
        cls.narrative = NarrativeTranslation()
        cls.narrative.save(author=cls.user)
    
    def login(self): 
        return self.client.force_login(self.user)
    
    def logout(self):
        return self.client.logout()