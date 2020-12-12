from django.test import TestCase
from model_bakery import baker
from django.shortcuts import reverse


class AuthorViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user, cls.author = baker.make('auth.User', _quantity=2)
    

    def setUp(self):
        self.client.logout()


    def test_authorview_anonymous(self):
        response = self.client.get(reverse('identity:author', kwargs={'username': self.author.username}))
        self.assertEqual(response.status_code, 200)
    
    
    def test_authorview_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('identity:author', kwargs={'username': self.author.username}))
        self.assertEqual(response.status_code, 200)
