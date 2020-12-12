from .common import TestCase
from django.shortcuts import reverse
import logging
from model_bakery import baker
from notebook.models import NarrativeTranslation
from django.contrib.auth.models import User

class NarrativeDetail(TestCase):

    def setUp(self):
        self.narrative.sketch = False
        self.narrative.title = 'Title'
        self.narrative.save()

    def test_narrative_detail_anonymous(self):
        self.logout()
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': self.narrative.slug}))
        self.assertEqual(response.status_code, 200, 'Status Code not 200 when accessing NarrativeDetail')
    
    def test_narrative_detail_authorized(self):
        self.login()
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': self.narrative.slug}))
        self.assertEqual(response.status_code, 200, 'Status Code not 200 when accessing NarrativeDetail')
    
    def test_narrative_detail_with_unrecognized_language_code(self):
        self.narrative.language = 'xx'
        self.narrative.save()
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': self.narrative.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_nonexistent_narrative(self):
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)

        
