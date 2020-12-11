from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from model_bakery import baker

class LandingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls): 
        cls.user = baker.make('auth.User')
    
    def login(self): 
        return self.client.force_login(self.user)
    
    def logout(self):
        return self.client.logout()
    
    def test_landing_anonymous(self):
        self.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_landing_reverse_anonymous(self):
        self.logout()
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
    
    def test_landing_authenticated(self):
        logged_in = self.login()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_landing_reverse_authenticated(self):
        logged_in = self.login()
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
