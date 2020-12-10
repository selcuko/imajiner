from imajiner.tests import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

class LandingTestCase(TestCase):
    
    def test_landing_anonymous(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_landing_reverse_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
    
    def test_landing_authenticated(self):
        logged_in = self.client.login(username='wanderman', password='birileriikigeri')
        self.assertEqual(logged_in, True)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_landing_reverse_authenticated(self):
        logged_in = self.client.login(username='wanderman', password='birileriikigeri')
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
