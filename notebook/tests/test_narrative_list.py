from .common import TestCase
from django.shortcuts import reverse
from notebook.models import Narrative, NarrativeTranslation
import random
from model_bakery import baker
import faker
import logging
from django.contrib.auth.models import User


class NarrativeListTest(TestCase):

    def test_list_anonymous(self):
        self.logout()
        response = self.client.get(reverse('narrative:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_authenticated(self):
        logged_in = self.login()
        response = self.client.get(reverse('narrative:list'))
        self.assertEqual(response.status_code, 200)