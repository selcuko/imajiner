from imajiner.tests import TestCase
from django.shortcuts import reverse
from notebook.models import Narrative, NarrativeTranslation
import random
from model_bakery import baker
import faker
import logging
from django.contrib.auth.models import User


class NarrativeListTest(TestCase):

    def test_list_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('narrative:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_authenticated(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertEqual(logged_in, True)
        response = self.client.get(reverse('narrative:list'))
        self.assertEqual(response.status_code, 200)