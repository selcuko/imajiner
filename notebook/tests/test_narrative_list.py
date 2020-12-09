from django.test import TestCase
from django.shortcuts import reverse
from notebook.models import Narrative, NarrativeTranslation
import random
from model_bakery import baker
import faker
import logging
from django.contrib.auth.models import User


class NarrativeListTest(TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        narrative_count = NarrativeTranslation.objects.all().count()
        if narrative_count < 100:
            self.logger.debug(f'NarrativeTranslation objects count ({narrative_count}) is less than 100, recreating.')
            baker.make(NarrativeTranslation, _quantity=100, _fill_optional=True, make_m2m=True)
        self.narratives = NarrativeTranslation.objects.all()
        self.username, self.password = 'wanderman', 'wanderman'
        self.user = User.objects.create_user(username=self.username, password=self.password)



    def test_list_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('narrative:list'))
        self.assertEquals(response.status_code, 200)

    def test_list_authenticated(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertEquals(logged_in, True)
        response = self.client.get(reverse('narrative:list'))
        self.assertEquals(response.status_code, 200)