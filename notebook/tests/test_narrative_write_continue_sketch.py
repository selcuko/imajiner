from .common import TestCase
from django.shortcuts import reverse
from model_bakery import baker
from ..models import NarrativeTranslation

class NarrativeContinueSketch(TestCase):

    def test_get_narrative_write_anonymous(self):
        self.logout()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 302)
    
    def test_get_narrative_write_authorized(self):
        self.login()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 200)

