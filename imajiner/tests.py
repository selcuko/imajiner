from django.test import TestCase as DjangoTestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation
from django.contrib.auth.models import User
import logging
from model_bakery import baker

class TestCase(DjangoTestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        narrative_count = NarrativeTranslation.objects.all().count()
        if narrative_count < 100:
            self.logger.debug(f'NarrativeTranslation objects count ({narrative_count}) is less than 100, recreating.')
            baker.make(NarrativeTranslation, sketch=False, _quantity=100, _fill_optional=True, make_m2m=True)
        self.narratives = NarrativeTranslation.objects.all()
        self.username, self.password = 'wanderman', 'wanderman'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def login(self):
        return self.client.login(username=self.username, password=self.password)
    
    def logout(self):
        return self.client.logout()