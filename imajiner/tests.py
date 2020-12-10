from django.test import TestCase as DjangoTestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation
from django.contrib.auth.models import User
import logging
from model_bakery import baker

logger = logging.getLogger(__name__)


class TestCase(DjangoTestCase):
    username, password = 'wanderman', 'wanderman'
    logger = logging.getLogger(__name__)
    
    @classmethod
    def setUpTestData(cls):
        logger.debug('Setting up test data.')
        cls.logger.setLevel(logging.DEBUG)

        user_exists = User.objects.filter(username=cls.username)
        if not user_exists:
            cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        else:
            cls.user = User.objects.get(username=cls.username)

        narrative_count = NarrativeTranslation.objects.all().count()
        if narrative_count < 100:
            cls.logger.debug(f'NarrativeTranslation objects count ({narrative_count}) is less than 100, recreating.')
            baker.make(NarrativeTranslation, master__author=cls.user, sketch=False, _quantity=100, _fill_optional=True, make_m2m=True)
        
        cls.narratives = NarrativeTranslation.objects.all()
        narrative_count = cls.narratives.count()
    
    
    def setUp(self):
        logger.debug('Assigning class attributes.')
        #self.narratives = NarrativeTranslation.objects.all()
        logger.debug(f'Total {self.narratives.count()} narratives are present in DB.')
        #self.user = User.objects.last()

    def login(self):
        return self.client.login(username=self.username, password=self.password)
    
    def logout(self):
        return self.client.logout()
    
    def tearDown(*args, **kwargs): pass
    def tearDownClass(*args, **kwargs): pass
    def doCleanups(*args, **kwargs): pass
    def tearDown(*args, **kwargs): pass