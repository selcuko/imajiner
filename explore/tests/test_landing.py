from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

class LandingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='wanderman', password='birileriikigeri') if not User.objects.filter(username='wanderman').exists() else User.objects.get(username='wanderman')
    
    def test_landing_anonymous(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
    
    def test_landing_reverse_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('landing'))
        self.assertEquals(response.status_code, 200)
    
    def test_landing_authenticated(self):
        logged_in = self.client.login(username='wanderman', password='birileriikigeri')
        self.assertEquals(logged_in, True)
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
    
    def test_landing_reverse_authenticated(self):
        logged_in = self.client.login(username='wanderman', password='birileriikigeri')
        self.assertEquals(logged_in, True)
        response = self.client.get(reverse('landing'))
        self.assertEquals(response.status_code, 200)
