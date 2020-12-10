from imajiner.tests import TestCase
from django.shortcuts import reverse
import logging
from model_bakery import baker
from notebook.models import NarrativeTranslation
from django.contrib.auth.models import User

class NarrativeDetail(TestCase):

    def test_narrative_detail_anonymous(self):
        self.logout()
        queryset = self.narratives.filter(sketch=False)
        narrative = queryset.first()
        assert narrative is not None, 'Test DB do not have any published narratives.'
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': narrative.slug}))
        assert response.status_code == 200, 'Status Code not 200 when accessing NarrativeDetail'
    
    def test_narrative_detail_authorized(self):
        self.login()
        queryset = self.narratives.filter(sketch=False)
        narrative = queryset.first()
        assert narrative is not None, 'Test DB do not have any published narratives.'
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': narrative.slug}))
        assert response.status_code == 200, 'Status Code not 200 when accessing NarrativeDetail'
    
    def test_narrative_detail_with_unrecognized_language_code(self):
        narrative = self.narratives.first()
        narrative.language = 'xx'
        narrative.save()
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': narrative.slug}))
        assert response.status_code == 200
    
    def test_nonexistent_narrative(self):
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': 'nönexistent'}))
        assert response.status_code == 404

        
